"""
JARVIS AI Assistant - Command Handler Module

This module handles command processing, parsing, and execution with support for
natural language understanding, command history, and intelligent routing.

Author: JARVIS AI Team
Version: 2.0.0
License: MIT
"""

import re
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommandType(Enum):
    """Types of commands that can be processed"""
    SYSTEM = "system"
    APPLICATION = "application"
    FILE = "file"
    PHONE = "phone"
    AI_QUERY = "ai_query"
    AUTOMATION = "automation"
    SETTINGS = "settings"
    UNKNOWN = "unknown"


class CommandPriority(Enum):
    """Command execution priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Command:
    """Represents a parsed command with metadata"""
    raw_text: str
    command_type: CommandType
    action: str
    parameters: Dict[str, Any]
    priority: CommandPriority = CommandPriority.NORMAL
    timestamp: datetime = None
    user_id: Optional[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class CommandResult:
    """Represents the result of command execution"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    error: Optional[str] = None


class CommandPattern:
    """Represents a command pattern for matching user input"""
    
    def __init__(self, pattern: str, command_type: CommandType, action: str, 
                 parameters: Optional[Dict[str, str]] = None):
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.command_type = command_type
        self.action = action
        self.parameters = parameters or {}
    
    def match(self, text: str) -> Optional[Tuple[Dict[str, Any], float]]:
        """
        Match text against this pattern.
        
        Args:
            text: Input text to match
            
        Returns:
            Tuple of (parameters, confidence) if match found, None otherwise
        """
        match = self.pattern.search(text)
        if match:
            params = match.groupdict()
            # Calculate confidence based on match quality
            confidence = len(match.group()) / len(text)
            return params, confidence
        return None


class CommandHistory:
    """Manages command history with SQLite database"""
    
    def __init__(self, db_path: str = "command_history.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the command history database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS command_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        raw_text TEXT NOT NULL,
                        command_type TEXT NOT NULL,
                        action TEXT NOT NULL,
                        parameters TEXT,
                        success BOOLEAN NOT NULL,
                        execution_time REAL,
                        user_id TEXT,
                        confidence REAL
                    )
                """)
                conn.commit()
            logger.info("Command history database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize command history database: {e}")
    
    def add_command(self, command: Command, result: CommandResult):
        """Add a command and its result to history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO command_history 
                    (timestamp, raw_text, command_type, action, parameters, 
                     success, execution_time, user_id, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    command.timestamp.isoformat(),
                    command.raw_text,
                    command.command_type.value,
                    command.action,
                    json.dumps(command.parameters),
                    result.success,
                    result.execution_time,
                    command.user_id,
                    command.confidence
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to add command to history: {e}")
    
    def get_recent_commands(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commands from history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM command_history 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get recent commands: {e}")
            return []
    
    def get_command_statistics(self) -> Dict[str, Any]:
        """Get command usage statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Total commands
                total = conn.execute("SELECT COUNT(*) FROM command_history").fetchone()[0]
                
                # Success rate
                success_count = conn.execute(
                    "SELECT COUNT(*) FROM command_history WHERE success = 1"
                ).fetchone()[0]
                success_rate = (success_count / total * 100) if total > 0 else 0
                
                # Most used commands
                most_used = conn.execute("""
                    SELECT action, COUNT(*) as count 
                    FROM command_history 
                    GROUP BY action 
                    ORDER BY count DESC 
                    LIMIT 5
                """).fetchall()
                
                # Command types distribution
                type_dist = conn.execute("""
                    SELECT command_type, COUNT(*) as count 
                    FROM command_history 
                    GROUP BY command_type
                """).fetchall()
                
                return {
                    "total_commands": total,
                    "success_rate": round(success_rate, 2),
                    "most_used_commands": [{"action": row[0], "count": row[1]} for row in most_used],
                    "command_types": [{"type": row[0], "count": row[1]} for row in type_dist]
                }
        except Exception as e:
            logger.error(f"Failed to get command statistics: {e}")
            return {}


class CommandHandler:
    """
    Advanced command handler with natural language processing,
    pattern matching, and intelligent command routing.
    """
    
    def __init__(self):
        self.patterns: List[CommandPattern] = []
        self.handlers: Dict[str, Callable] = {}
        self.history = CommandHistory()
        self.is_processing = False
        self.processing_lock = threading.Lock()
        
        # Initialize default command patterns
        self._initialize_patterns()
        
        logger.info("CommandHandler initialized")
    
    def _initialize_patterns(self):
        """Initialize default command patterns"""
        # System commands
        self.add_pattern(
            r"open\s+(?P<app_name>[\w\s]+)",
            CommandType.APPLICATION,
            "open_application",
            {"app_name": "app_name"}
        )
        
        self.add_pattern(
            r"close\s+(?P<app_name>[\w\s]+)",
            CommandType.APPLICATION,
            "close_application",
            {"app_name": "app_name"}
        )
        
        self.add_pattern(
            r"take\s+(?:a\s+)?screenshot",
            CommandType.SYSTEM,
            "take_screenshot"
        )
        
        self.add_pattern(
            r"(?:show|get|display)\s+system\s+(?:stats|status|info)",
            CommandType.SYSTEM,
            "get_system_info"
        )
        
        # File operations
        self.add_pattern(
            r"(?:create|make)\s+(?:a\s+)?file\s+(?:named\s+)?(?P<filename>[\w\.\-]+)",
            CommandType.FILE,
            "create_file",
            {"filename": "filename"}
        )
        
        self.add_pattern(
            r"(?:delete|remove)\s+(?:file\s+)?(?P<filename>[\w\.\-\s]+)",
            CommandType.FILE,
            "delete_file",
            {"filename": "filename"}
        )
        
        # Phone commands
        self.add_pattern(
            r"(?:send\s+)?(?:message|text)\s+(?:to\s+)?(?P<contact>[\w\s]+)",
            CommandType.PHONE,
            "send_message",
            {"contact": "contact"}
        )
        
        self.add_pattern(
            r"(?:call|phone)\s+(?P<contact>[\w\s]+)",
            CommandType.PHONE,
            "make_call",
            {"contact": "contact"}
        )
        
        # AI queries (catch-all for questions)
        self.add_pattern(
            r"(?:what|how|why|when|where|who|can\s+you|tell\s+me|explain).*",
            CommandType.AI_QUERY,
            "ai_query"
        )
        
        # Settings commands
        self.add_pattern(
            r"(?:set|change)\s+(?:voice\s+)?(?:to\s+)?(?P<setting>male|female)",
            CommandType.SETTINGS,
            "set_voice_gender",
            {"gender": "setting"}
        )
        
        self.add_pattern(
            r"(?:set|change)\s+volume\s+(?:to\s+)?(?P<volume>\d+)",
            CommandType.SETTINGS,
            "set_volume",
            {"volume": "volume"}
        )
        
        logger.info(f"Initialized {len(self.patterns)} command patterns")
    
    def add_pattern(self, pattern: str, command_type: CommandType, action: str, 
                   parameters: Optional[Dict[str, str]] = None):
        """
        Add a new command pattern.
        
        Args:
            pattern: Regular expression pattern
            command_type: Type of command
            action: Action to execute
            parameters: Parameter mapping
        """
        try:
            cmd_pattern = CommandPattern(pattern, command_type, action, parameters)
            self.patterns.append(cmd_pattern)
            logger.info(f"Added command pattern: {action}")
        except Exception as e:
            logger.error(f"Failed to add command pattern: {e}")
    
    def register_handler(self, action: str, handler: Callable[[Command], CommandResult]):
        """
        Register a command handler function.
        
        Args:
            action: Action name to handle
            handler: Handler function
        """
        self.handlers[action] = handler
        logger.info(f"Registered handler for action: {action}")
    
    def parse_command(self, text: str, user_id: Optional[str] = None) -> Optional[Command]:
        """
        Parse text input into a Command object.
        
        Args:
            text: Input text to parse
            user_id: Optional user identifier
            
        Returns:
            Parsed Command object or None if no match found
        """
        if not text or not text.strip():
            return None
        
        text = text.strip()
        best_match = None
        best_confidence = 0.0
        
        # Try to match against all patterns
        for pattern in self.patterns:
            match_result = pattern.match(text)
            if match_result:
                params, confidence = match_result
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = (pattern, params, confidence)
        
        if best_match:
            pattern, params, confidence = best_match
            
            # Create command object
            command = Command(
                raw_text=text,
                command_type=pattern.command_type,
                action=pattern.action,
                parameters=params,
                confidence=confidence,
                user_id=user_id
            )
            
            logger.info(f"Parsed command: {command.action} (confidence: {confidence:.2f})")
            return command
        
        # If no pattern matches, treat as AI query
        logger.info(f"No pattern match found, treating as AI query: {text}")
        return Command(
            raw_text=text,
            command_type=CommandType.AI_QUERY,
            action="ai_query",
            parameters={"query": text},
            confidence=0.5,
            user_id=user_id
        )
    
    def execute_command(self, command: Command) -> CommandResult:
        """
        Execute a parsed command.
        
        Args:
            command: Command to execute
            
        Returns:
            CommandResult with execution details
        """
        start_time = time.time()
        
        try:
            with self.processing_lock:
                self.is_processing = True
                
                # Check if handler exists
                if command.action in self.handlers:
                    handler = self.handlers[command.action]
                    result = handler(command)
                else:
                    # Default handling for unregistered actions
                    result = self._default_handler(command)
                
                # Calculate execution time
                execution_time = time.time() - start_time
                result.execution_time = execution_time
                
                # Add to history
                self.history.add_command(command, result)
                
                logger.info(f"Command executed: {command.action} "
                          f"(success: {result.success}, time: {execution_time:.3f}s)")
                
                return result
                
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = CommandResult(
                success=False,
                message=f"Command execution failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )
            
            # Add failed command to history
            self.history.add_command(command, error_result)
            
            logger.error(f"Command execution error: {e}")
            return error_result
            
        finally:
            self.is_processing = False
    
    def _default_handler(self, command: Command) -> CommandResult:
        """
        Default handler for commands without registered handlers.
        
        Args:
            command: Command to handle
            
        Returns:
            CommandResult indicating the command needs a handler
        """
        return CommandResult(
            success=False,
            message=f"No handler registered for action: {command.action}",
            error="HANDLER_NOT_FOUND"
        )
    
    def process_text(self, text: str, user_id: Optional[str] = None) -> CommandResult:
        """
        Process text input end-to-end (parse + execute).
        
        Args:
            text: Input text to process
            user_id: Optional user identifier
            
        Returns:
            CommandResult from execution
        """
        # Parse command
        command = self.parse_command(text, user_id)
        
        if not command:
            return CommandResult(
                success=False,
                message="Could not parse command",
                error="PARSE_FAILED"
            )
        
        # Execute command
        return self.execute_command(command)
    
    def get_command_suggestions(self, partial_text: str, limit: int = 5) -> List[str]:
        """
        Get command suggestions based on partial input.
        
        Args:
            partial_text: Partial command text
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested commands
        """
        suggestions = []
        
        try:
            # Get recent commands that start with partial text
            recent_commands = self.history.get_recent_commands(50)
            
            for cmd in recent_commands:
                if cmd['raw_text'].lower().startswith(partial_text.lower()):
                    if cmd['raw_text'] not in suggestions:
                        suggestions.append(cmd['raw_text'])
                        if len(suggestions) >= limit:
                            break
            
            # Add common command templates if not enough suggestions
            if len(suggestions) < limit:
                common_commands = [
                    "open calculator",
                    "take screenshot",
                    "show system status",
                    "send message to",
                    "what's the weather",
                    "set volume to 50",
                    "close chrome"
                ]
                
                for cmd in common_commands:
                    if cmd.startswith(partial_text.lower()) and cmd not in suggestions:
                        suggestions.append(cmd)
                        if len(suggestions) >= limit:
                            break
            
        except Exception as e:
            logger.error(f"Failed to get command suggestions: {e}")
        
        return suggestions[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get command processing statistics"""
        return self.history.get_command_statistics()
    
    def get_recent_commands(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent command history"""
        return self.history.get_recent_commands(limit)
    
    def clear_history(self) -> bool:
        """Clear command history"""
        try:
            with sqlite3.connect(self.history.db_path) as conn:
                conn.execute("DELETE FROM command_history")
                conn.commit()
            logger.info("Command history cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear command history: {e}")
            return False
    
    def export_history(self, filepath: str) -> bool:
        """
        Export command history to JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if exported successfully, False otherwise
        """
        try:
            commands = self.history.get_recent_commands(1000)  # Export last 1000 commands
            
            with open(filepath, 'w') as f:
                json.dump(commands, f, indent=2, default=str)
            
            logger.info(f"Command history exported to: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export command history: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Initialize command handler
    handler = CommandHandler()
    
    # Register some example handlers
    def open_app_handler(command: Command) -> CommandResult:
        app_name = command.parameters.get('app_name', 'unknown')
        return CommandResult(
            success=True,
            message=f"Opening {app_name}",
            data={"app_name": app_name}
        )
    
    def ai_query_handler(command: Command) -> CommandResult:
        query = command.parameters.get('query', command.raw_text)
        return CommandResult(
            success=True,
            message=f"Processing AI query: {query}",
            data={"query": query}
        )
    
    # Register handlers
    handler.register_handler("open_application", open_app_handler)
    handler.register_handler("ai_query", ai_query_handler)
    
    # Test commands
    test_commands = [
        "open calculator",
        "open notepad",
        "what's the weather today?",
        "take a screenshot",
        "send message to John",
        "how are you doing?"
    ]
    
    print("Testing command processing...")
    for cmd_text in test_commands:
        print(f"\nInput: {cmd_text}")
        result = handler.process_text(cmd_text, user_id="test_user")
        print(f"Result: {result.message} (Success: {result.success})")
    
    # Show statistics
    print("\nCommand Statistics:")
    stats = handler.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Show recent commands
    print("\nRecent Commands:")
    recent = handler.get_recent_commands(5)
    for cmd in recent:
        print(f"  - {cmd['raw_text']} ({cmd['command_type']})")
    
    print("\nCommand handler test completed")