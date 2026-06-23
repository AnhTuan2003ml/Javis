$(document).ready(function () {



    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message").text(message);
        $('.siri-message').textillate('start');
        
        // Update face auth status in settings
        if (message.includes("Face recognition is currently enabled")) {
            $("#faceAuthStatus").text("Enabled").css("color", "#00ff00");
        } else if (message.includes("Face recognition is currently disabled")) {
            $("#faceAuthStatus").text("Disabled").css("color", "#ff0000");
        }

    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }
    
    // Show continuous listening view
    eel.expose(ShowContinuousListen)
    function ShowContinuousListen() {
        $("#Oval").attr("hidden", true);
        $("#ContinuousListen").attr("hidden", false);
    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }

    
    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader)
    function hideLoader() {

        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);

    }
    // Hide Face auth and display Face Auth success animation
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {

        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);

    }
    // Hide success and display 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {

        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);

    }


    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");

        }, 1000)
        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000)
    }

    // AI Provider Controls
    $("#setGroqAI").click(function() {
        eel.setAIProvider("groq")(function(result) {
            $("#currentAIProvider").text("GROQ");
            alert(result);
        });
    });
    
    $("#setGeminiAI").click(function() {
        eel.setAIProvider("gemini")(function(result) {
            $("#currentAIProvider").text("GEMINI");
            alert(result);
        });
    });
    
    // Load AI provider status on page load
    eel.getAIProvider()(function(provider) {
        $("#currentAIProvider").text(provider.toUpperCase());
    });
    
    // Response Style Controls
    $(".style-btn").click(function() {
        const style = $(this).data('style');
        eel.setResponseStyle(style)(function(result) {
            $("#currentResponseStyle").text(style.toUpperCase());
            alert(result);
        });
    });
    
    // AI Personality Controls
    $(".personality-btn").click(function() {
        const personality = $(this).data('personality');
        eel.setAIPersonality(personality)(function(result) {
            $("#currentAIPersonality").text(personality.toUpperCase());
            alert(result);
        });
    });
    
    // Load personality settings on page load
    eel.getPersonalitySettings()(function(settings) {
        $("#currentResponseStyle").text(settings.response_style.toUpperCase());
        $("#currentAIPersonality").text(settings.ai_personality.toUpperCase());
    });
    
    // Continuous listening buttons
    $("#ContinuousStartBtn").click(function () {
        eel.startContinuousListen()(function(result) {
            if (result && !result.startsWith('Error')) {
                $("#Oval").attr("hidden", true);
                $("#ContinuousListen").attr("hidden", false);
                $(".continuous-message").text('🎤 Listening...');
                $("#ContinuousStartBtn").hide();
            }
        });
    });
    
    $(document).on('click', '#ContinuousStopBtn', function () {
        eel.stopContinuousListen()(function(result) {
            $("#ContinuousListen").attr("hidden", true);
            $("#Oval").attr("hidden", false);
            $("#ContinuousStartBtn").show();
        });
    });
    
    eel.expose(updateListenStatus)
    function updateListenStatus(status) {
        $(".continuous-message").text(status);
    }
    
    // Command History Functions
    function loadCommandHistory() {
        eel.getCommandHistory()(function(history) {
            displayCommandHistory(history);
        });
    }
    
    function loadStatistics() {
        eel.getCommandStatistics()(function(stats) {
            displayStatistics(stats);
        });
    }
    
    function searchCommands() {
        const query = document.getElementById('searchQuery').value;
        const dateFilter = document.getElementById('dateFilter').value;
        const typeFilter = document.getElementById('typeFilter').value;
        
        eel.searchCommands(query, dateFilter, typeFilter)(function(results) {
            displayCommandHistory(results);
        });
    }
    
    function displayStatistics(stats) {
        const statsHtml = `
            <div class="mb-3 p-3" style="background: rgba(0,170,255,0.1); border-radius: 10px; border-left: 3px solid #00AAFF;">
                <h6 class="text-light mb-2">📊 Statistics</h6>
                <div class="row text-center">
                    <div class="col-3"><small class="text-muted">Total</small><br><span class="text-light">${stats.total}</span></div>
                    <div class="col-3"><small class="text-muted">Voice</small><br><span class="text-info">${stats.voice}</span></div>
                    <div class="col-3"><small class="text-muted">Text</small><br><span class="text-warning">${stats.text}</span></div>
                    <div class="col-3"><small class="text-muted">Success</small><br><span class="text-success">${stats.success_rate}%</span></div>
                </div>
                ${stats.most_used.length > 0 ? `<div class="mt-2"><small class="text-muted">Most Used:</small> ${stats.most_used.map(cmd => cmd[0]).join(', ')}</div>` : ''}
            </div>`;
        
        const existingStats = document.querySelector('.stats-container');
        if (existingStats) existingStats.remove();
        
        const chatBox = document.getElementById("chat-canvas-body");
        const statsDiv = document.createElement('div');
        statsDiv.className = 'stats-container';
        statsDiv.innerHTML = statsHtml;
        chatBox.insertBefore(statsDiv, chatBox.firstChild);
    }
    
    function displayCommandHistory(history) {
        var chatBox = document.getElementById("chat-canvas-body");
        
        // Remove existing content except stats
        const statsContainer = chatBox.querySelector('.stats-container');
        chatBox.innerHTML = '';
        if (statsContainer) chatBox.appendChild(statsContainer);
        
        // Add toggle buttons
        chatBox.innerHTML += `
            <div class="text-center mb-3">
                <button id="toggleStats" class="btn btn-sm btn-outline-info me-2">📊 Statistics</button>
                <button id="toggleSearch" class="btn btn-sm btn-outline-warning me-2">🔍 Search</button>
                <button id="clearHistoryBtn" class="btn btn-sm btn-outline-danger">🗑️ Clear All</button>
            </div>`;
        
        // Add search/filter controls (hidden by default)
        chatBox.innerHTML += `
            <div id="searchControls" class="mb-3 p-2" style="background: rgba(255,255,255,0.05); border-radius: 8px; display: none;">
                <div class="row g-2">
                    <div class="col-12"><input type="text" id="searchQuery" class="form-control form-control-sm" placeholder="🔍 Search commands..." style="background: rgba(0,0,0,0.3); border: 1px solid #00AAFF; color: white;"></div>
                    <div class="col-6">
                        <select id="dateFilter" class="form-select form-select-sm" style="background: rgba(0,0,0,0.3); border: 1px solid #00AAFF; color: white;">
                            <option value="">All Time</option>
                            <option value="today">Today</option>
                            <option value="week">This Week</option>
                            <option value="month">This Month</option>
                        </select>
                    </div>
                    <div class="col-6">
                        <select id="typeFilter" class="form-select form-select-sm" style="background: rgba(0,0,0,0.3); border: 1px solid #00AAFF; color: white;">
                            <option value="">All Types</option>
                            <option value="voice">🎤 Voice</option>
                            <option value="text">⌨️ Text</option>
                        </select>
                    </div>
                </div>
            </div>`;
        
        if (history && history.length > 0) {
            // Display each command
            history.forEach(function(entry) {
                const timestamp = new Date(entry.timestamp).toLocaleString();
                const inputType = entry.input_type === 'voice' ? '🎤' : '⌨️';
                
                // User input
                chatBox.innerHTML += `<div class="row justify-content-end mb-2">
                    <div class="width-size">
                        <div class="sender_message">
                            <small class="text-muted">${inputType} ${timestamp}</small><br>
                            ${entry.user_input}
                        </div>
                    </div>
                </div>`;
                
                // Jarvis response
                if (entry.jarvis_response && entry.jarvis_response !== "Processing...") {
                    chatBox.innerHTML += `<div class="row justify-content-start mb-3">
                        <div class="width-size">
                            <div class="receiver_message">${entry.jarvis_response}</div>
                        </div>
                    </div>`;
                }
            });
        } else {
            chatBox.innerHTML += `<div class="text-center text-light mt-5">
                <h5>📝 No Commands Found</h5>
                <p class="text-muted">Try adjusting your search filters</p>
            </div>`;
        }
        
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
        
        // Add event listeners
        $(document).off('click', '#toggleStats').on('click', '#toggleStats', function() {
            if ($('.stats-container').is(':visible')) {
                $('.stats-container').hide();
            } else {
                loadStatistics();
                $('.stats-container').show();
            }
        });
        
        $(document).off('click', '#toggleSearch').on('click', '#toggleSearch', function() {
            $('#searchControls').toggle();
        });
        
        $(document).off('input', '#searchQuery').on('input', '#searchQuery', function() {
            searchCommands();
        });
        $(document).off('change', '#dateFilter, #typeFilter').on('change', '#dateFilter, #typeFilter', searchCommands);
        $(document).off('click', '#clearHistoryBtn').on('click', '#clearHistoryBtn', function() {
            if (confirm('Are you sure you want to clear all command history?')) {
                eel.clearCommandHistory()(function(result) {
                    loadCommandHistory();
                });
            }
        });
        
        // Hide stats and search by default
        setTimeout(function() {
            $('.stats-container').hide();
            $('#searchControls').hide();
        }, 100);
    }
    
    // Load command history when chat panel opens
    $(document).on('show.bs.offcanvas', '#offcanvasScrolling', function() {
        loadCommandHistory();
    });

});
// Add function to read config files
eel.expose(readConfigFiles);
function readConfigFiles() {
    return new Promise((resolve) => {
        const configs = {};
        
        // Try to read AI config
        try {
            fetch('file:///C:/Users/Hp/Music/inp/ai_config.json')
                .then(response => response.json())
                .then(data => {
                    configs.ai_config = data;
                })
                .catch(() => {
                    configs.ai_config = { provider: 'GROQ' };
                });
        } catch (e) {
            configs.ai_config = { provider: 'GROQ' };
        }
        
        // Try to read voice config
        try {
            fetch('file:///C:/Users/Hp/Music/inp/voice_config.json')
                .then(response => response.json())
                .then(data => {
                    configs.voice_config = data;
                })
                .catch(() => {
                    configs.voice_config = { gender: 'male' };
                });
        } catch (e) {
            configs.voice_config = { gender: 'male' };
        }
        
        // Try to read language
        try {
            fetch('file:///C:/Users/Hp/Music/inp/current_language.txt')
                .then(response => response.text())
                .then(data => {
                    configs.language = data.trim() || 'english';
                })
                .catch(() => {
                    configs.language = 'english';
                });
        } catch (e) {
            configs.language = 'english';
        }
        
        setTimeout(() => resolve(configs), 100);
    });
}
// Add function to read command history
eel.expose(readCommandHistory);
function readCommandHistory() {
    return new Promise((resolve) => {
        try {
            fetch('file:///C:/Users/Hp/Music/inp/command_history.json')
                .then(response => response.json())
                .then(data => {
                    resolve(data);
                })
                .catch(() => {
                    resolve([]);
                });
        } catch (e) {
            resolve([]);
        }
    });
}