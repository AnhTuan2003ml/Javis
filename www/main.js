$(document).ready(function () {

    eel.init()()

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
      });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event
    window.jarvisMicFunction = function() {
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    };

    $("#MicBtn").click(function () { 
        window.jarvisMicFunction();
    });
    
    // Face recognition toggle buttons (if you want UI buttons)
    $("#FaceAuthOn").click(function () {
        eel.allCommands("turn on face recognition")
    });
    
    $("#FaceAuthOff").click(function () {
        eel.allCommands("turn off face recognition")
    });
    
    $("#FaceAuthStatus").click(function () {
        eel.allCommands("face recognition status")
    });


    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });


    
    // Close settings modal
    $("#closeSettings").click(function () {
        $("#settingsModal").hide();
    });
    
    // Biometric authentication toggle buttons
    $("#enableFaceAuth").click(function () {
        eel.enableFaceAuth()();
        updateFaceAuthStatus("Enabled");
    });
    
    $("#disableFaceAuth").click(function () {
        eel.disableFaceAuth()();
        updateFaceAuthStatus("Disabled");
    });
    
    $("#enableFingerprintAuth").click(function () {
        eel.enableFingerprintAuth()();
        updateFingerprintAuthStatus("Enabled");
    });
    
    $("#disableFingerprintAuth").click(function () {
        eel.disableFingerprintAuth()();
        updateFingerprintAuthStatus("Disabled");
    });
    
    // Functions to update auth status in UI
    function updateFaceAuthStatus(status) {
        if (status === "Enabled") {
            $("#faceAuthStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#faceAuthStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    function updateFingerprintAuthStatus(status) {
        if (status === "Enabled") {
            $("#fingerprintAuthStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#fingerprintAuthStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    // Function to check and display current auth status
    function checkAuthStatus() {
        eel.getFaceAuthStatus()(updateFaceAuthStatus);
        eel.getFingerprintAuthStatus()(updateFingerprintAuthStatus);
    }
    
    // Check status when settings modal opens
    $("#SettingsBtn").click(function () {
        $("#settingsModal").show();
        setTimeout(function() {
            checkAllStatus();
        }, 100);
    });
    
    // Voice gender buttons
    $("#setMaleVoice").click(function () {
        eel.setVoiceGender("male")();
        updateVoiceGender("Male");
    });
    
    $("#setFemaleVoice").click(function () {
        eel.setVoiceGender("female")();
        updateVoiceGender("Female");
    });
    
    // Language selection buttons
    $(".lang-btn").click(function () {
        const language = $(this).data("lang");
        eel.setLanguage(language)();
        updateCurrentLanguage(language.charAt(0).toUpperCase() + language.slice(1));
    });
    
    // Toggle more languages
    $("#toggleMoreLangs").click(function () {
        const container = $("#moreLangsContainer");
        const button = $(this);
        
        if (container.is(":visible")) {
            container.hide();
            button.text("Show");
        } else {
            container.show();
            button.text("Hide");
        }
    });
    
    // Auto-start buttons
    $("#enableAutoStart").click(function () {
        eel.enableAutoStart()(function(result) {
            updateAutoStartStatus("Enabled");
        });
    });
    
    $("#disableAutoStart").click(function () {
        eel.disableAutoStart()(function(result) {
            updateAutoStartStatus("Disabled");
        });
    });
    
    // Phone notification buttons
    $("#enablePhoneNotifications").click(function () {
        eel.enablePhoneNotifications()(function(result) {
            updatePhoneNotificationStatus("Enabled");
        });
    });
    
    $("#disablePhoneNotifications").click(function () {
        eel.disablePhoneNotifications()(function(result) {
            updatePhoneNotificationStatus("Disabled");
        });
    });
    
    // SMS reading buttons
    $("#enableSmsReading").click(function () {
        eel.enableSmsReading()(function(result) {
            updateSmsReadingStatus("Enabled");
        });
    });
    
    $("#disableSmsReading").click(function () {
        eel.disableSmsReading()(function(result) {
            updateSmsReadingStatus("Disabled");
        });
    });
    
    // Call notification buttons
    $("#enableCallNotifications").click(function () {
        eel.enableCallNotifications()(function(result) {
            updateCallNotificationStatus("Enabled");
        });
    });
    
    $("#disableCallNotifications").click(function () {
        eel.disableCallNotifications()(function(result) {
            updateCallNotificationStatus("Disabled");
        });
    });
    
    // Functions to update voice and language status
    function updateVoiceGender(gender) {
        $("#voiceGender").text(gender);
    }
    
    function updateCurrentLanguage(language) {
        $("#currentLanguage").text(language);
    }
    
    function updateAutoStartStatus(status) {
        if (status === "Enabled") {
            $("#autoStartStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#autoStartStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    function updatePhoneNotificationStatus(status) {
        if (status === "Enabled") {
            $("#phoneNotificationStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#phoneNotificationStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    function updateSmsReadingStatus(status) {
        if (status === "Enabled") {
            $("#smsReadingStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#smsReadingStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    function updateCallNotificationStatus(status) {
        if (status === "Enabled") {
            $("#callNotificationStatus").text("Enabled").css("color", "#00ff00");
        } else {
            $("#callNotificationStatus").text("Disabled").css("color", "#ff0000");
        }
    }
    
    // Function to check voice and language status
    function checkVoiceLanguageStatus() {
        eel.getVoiceGender()(updateVoiceGender);
        eel.getCurrentLanguage()(updateCurrentLanguage);
        eel.getAutoStartStatus()(updateAutoStartStatus);
        eel.getPhoneNotificationStatus()(updatePhoneNotificationStatus);
        eel.getSmsReadingStatus()(updateSmsReadingStatus);
        eel.getCallNotificationStatus()(updateCallNotificationStatus);
    }
    
    // Audio and UI settings buttons
    $(".speed-btn").click(function () {
        const speed = $(this).data("speed");
        eel.setVoiceSpeed(speed)();
        updateVoiceSpeed(speed.charAt(0).toUpperCase() + speed.slice(1));
    });
    
    $(".volume-btn").click(function () {
        const volume = $(this).data("volume");
        eel.setVoiceVolume(volume)();
        updateVoiceVolume(volume.charAt(0).toUpperCase() + volume.slice(1));
    });
    

    
    // Functions to update UI settings status
    function updateVoiceSpeed(speed) {
        $("#voiceSpeed").text(speed);
    }
    
    function updateVoiceVolume(volume) {
        $("#voiceVolume").text(volume);
    }
    

    

    

    

    

    

    
    // Updated check status function
    function checkAllStatus() {
        checkAuthStatus();
        checkVoiceLanguageStatus();
        checkUISettings();
    }
    
    function checkUISettings() {
        eel.getVoiceSpeed()(updateVoiceSpeed);
        eel.getVoiceVolume()(updateVoiceVolume);
    }
    

    

    
    // Professional JARVIS Interface
    let systemMetrics = { cpu: 45, ram: 62, memory: 34 };
    let currentUser = 'Sir';
    
    // Update real-time data
    function updateRealTimeData() {
        // Update time
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: true });
        const dateStr = now.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        $('#currentTime').text(timeStr);
        $('#currentDate').text(dateStr);
        
        // Update greeting based on time
        const hour = now.getHours();
        let greeting = 'Good Evening';
        if (hour >= 5 && hour < 12) greeting = 'Good Morning';
        else if (hour >= 12 && hour < 17) greeting = 'Good Afternoon';
        else if (hour >= 17 && hour < 21) greeting = 'Good Evening';
        else greeting = 'Good Night';
        
        $('#greetingText').text(greeting + ' ' + currentUser);
    }
    
    // Update system metrics with real data
    function updateSystemMetrics() {
        eel.getSystemStats()(function(stats) {
            if (stats) {
                // Update CPU
                $('#cpuBar').css('width', stats.cpu + '%');
                $('#cpuValue').text(stats.cpu + '%');
                
                // Update CPU temperature
                const tempPercent = Math.min((stats.cpu_temp / 100) * 100, 100);
                $('#cpuTempBar').css('width', tempPercent + '%');
                $('#cpuTemp').text(stats.cpu_temp + '°C');
                
                // Update RAM
                const ramPercent = Math.round((stats.ram_used / stats.ram_total) * 100);
                $('#ramBar').css('width', ramPercent + '%');
                $('#ramValue').text((stats.ram_used / (1024**3)).toFixed(1) + ' GB');
                
                // Update Memory (Disk)
                const memoryPercent = Math.round((stats.disk_used / stats.disk_total) * 100);
                $('#memoryBar').css('width', memoryPercent + '%');
                $('#memoryValue').text((stats.disk_used / (1024**3)).toFixed(0) + '/' + (stats.disk_total / (1024**3)).toFixed(0) + ' GB');
            }
        });
    }
    
    // Update voice level
    function updateVoiceLevel() {
        voiceLevel = Math.floor(Math.random() * 60) + 20;
        $('.level-text').text(voiceLevel + '%');
        
        // Animate voice bars based on level
        $('.bar').each(function(index) {
            const height = Math.floor(Math.random() * 20) + 8;
            $(this).css('height', height + 'px');
        });
    }
    
    // Update emotion
    function updateEmotion(emotion = 'neutral') {
        const emotions = {
            happy: { icon: '😊', text: 'Happy' },
            sad: { icon: '😢', text: 'Sad' },
            excited: { icon: '🤩', text: 'Excited' },
            neutral: { icon: '😐', text: 'Neutral' },
            focused: { icon: '🤔', text: 'Focused' }
        };
        
        const current = emotions[emotion] || emotions.neutral;
        $('.emotion-icon').text(current.icon);
        $('.emotion-text').text(current.text);
        currentEmotion = emotion;
    }
    
    // Show processing
    function showProcessing(command) {
        isProcessing = true;
        $('#taskStatus').text(command);
        $('#processingBar').css('width', '0%').animate({ width: '100%' }, 2000);
        
        const startTime = Date.now();
        setTimeout(() => {
            isProcessing = false;
            $('#taskStatus').text('Ready');
            $('#processingBar').css('width', '0%');
            $('#responseMs').text((Date.now() - startTime) + 'ms');
        }, 2000);
    }
    
    // Quick actions
    $('.quick-action').click(function() {
        const cmd = $(this).data('cmd');
        showProcessing(cmd.charAt(0).toUpperCase() + cmd.slice(1));
        updateEmotion('focused');
        eel.allCommands(cmd);
    });
    
    // Start updates
    setInterval(updateSystemMetrics, 2000);
    setInterval(updateVoiceLevel, 800);
    
    // Override mic button for new interface
    $('#micBtn').click(function() {
        $('#listeningStatus').text('Processing voice command...');
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands()();
    });
    
    // Original mic button still works
    $('#MicBtn').off('click').click(function() {
        $('#listeningStatus').text('Processing voice command...');
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands()();
    });
    
    // Override send button
    $('#SendBtn').off('click').click(function() {
        const message = $('#chatbox').val();
        if (message) {
            showProcessing(message.length > 15 ? message.substring(0, 15) + '...' : message);
            updateEmotion('focused');
            eel.allCommands(message);
            $('#chatbox').val('');
            $('#MicBtn').attr('hidden', false);
            $('#SendBtn').attr('hidden', true);
        }
    });
    
    // Override enter key
    $('#chatbox').off('keypress').keypress(function(e) {
        if (e.which == 13) {
            const message = $('#chatbox').val();
            if (message) {
                showProcessing(message.length > 15 ? message.substring(0, 15) + '...' : message);
                updateEmotion('focused');
                eel.allCommands(message);
                $('#chatbox').val('');
                $('#MicBtn').attr('hidden', false);
                $('#SendBtn').attr('hidden', true);
            }
        }
    });
    
    // Initialize professional interface
    setTimeout(function() {
        checkAllStatus();
        updateSystemMetrics();
        updateRealTimeData();
    }, 2000);
    
    // Battery status function
    function updateBatteryStatus() {
        if ('getBattery' in navigator) {
            navigator.getBattery().then(function(battery) {
                const level = Math.round(battery.level * 100);
                const charging = battery.charging;
                
                $('#batteryLevel').css('width', level + '%');
                $('#batteryText').text(level + '%');
                
                // Change color based on battery level
                if (level > 50) {
                    $('#batteryLevel').css('background', 'linear-gradient(90deg, #2ed573, #26de81)');
                } else if (level > 20) {
                    $('#batteryLevel').css('background', 'linear-gradient(90deg, #ffa502, #ff6348)');
                } else {
                    $('#batteryLevel').css('background', 'linear-gradient(90deg, #ff4757, #ff3742)');
                }
                
                // Add charging indicator
                if (charging) {
                    $('#batteryText').text(level + '% ⚡');
                }
            }).catch(function() {
                // Fallback for unsupported browsers
                $('#batteryText').text('N/A');
                $('#batteryLevel').css('width', '0%');
            });
        } else {
            // Fallback for unsupported browsers
            $('#batteryText').text('N/A');
            $('#batteryLevel').css('width', '0%');
        }
    }
    
    // Start real-time updates
    setInterval(updateRealTimeData, 1000);
    setInterval(updateSystemMetrics, 5000);
    setInterval(updateBatteryStatus, 30000); // Update battery every 30 seconds
    
    // Initial battery update
    setTimeout(updateBatteryStatus, 1000);
    
    // Weather function for Belgaum
    function updateWeather() {
        const apiKey = 'your_api_key_here'; // Replace with actual API key
        const city = 'Belgaum';
        const country = 'IN';
        
        // Using OpenWeatherMap API (free tier)
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city},${country}&appid=${apiKey}&units=metric`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const temp = Math.round(data.main.temp);
                const description = data.weather[0].main;
                const humidity = data.main.humidity;
                
                $('#weatherText').text(`${temp}°C Belgaum, IN`);
                
                // Update weather icon based on condition
                const iconMap = {
                    'Clear': 'bi-sun',
                    'Clouds': 'bi-cloud',
                    'Rain': 'bi-cloud-rain',
                    'Thunderstorm': 'bi-cloud-lightning',
                    'Snow': 'bi-cloud-snow',
                    'Mist': 'bi-cloud-fog',
                    'Fog': 'bi-cloud-fog'
                };
                
                const iconClass = iconMap[description] || 'bi-cloud-sun';
                $('#weatherIcon').attr('class', `bi ${iconClass}`);
            })
            .catch(error => {
                // Fallback weather data for Belgaum
                $('#weatherText').text('28°C Belgaum, IN');
                $('#weatherIcon').attr('class', 'bi bi-cloud-sun');
            });
    }
    
    // Update weather every 10 minutes
    setTimeout(updateWeather, 2000);
    setInterval(updateWeather, 600000);
    
    // Get user name from backend
    function getUserName() {
        eel.getUserName()(function(name) {
            if (name && name !== 'Sir') {
                currentUser = name;
                updateRealTimeData();
            }
        });
    }
    
    // Update user name after face authentication
    window.updateUserAfterAuth = function(userId) {
        eel.getAuthenticatedUserName(userId)(function(name) {
            if (name && name !== 'Sir') {
                currentUser = name;
                updateRealTimeData();
                // Show welcome message with user name
                showWelcomeMessage(name);
                // Also update WishMessage in Start section
                updateWishMessage(name);
            }
        });
    }
    
    // Show personalized welcome message
    function showWelcomeMessage(userName) {
        const welcomeMsg = `Welcome back, ${userName}! How can I assist you today?`;
        $('.welcome-text').text(welcomeMsg);
        
        // Optional: Show a brief notification
        if (typeof eel !== 'undefined') {
            eel.speak(`Welcome back ${userName}`);
        }
    }
    
    // Update WishMessage in Start section
    function updateWishMessage(userName) {
        const hour = new Date().getHours();
        let greeting = 'Good Evening';
        if (hour >= 5 && hour < 12) greeting = 'Good Morning';
        else if (hour >= 12 && hour < 17) greeting = 'Good Afternoon';
        else if (hour >= 17 && hour < 21) greeting = 'Good Evening';
        else greeting = 'Good Night';
        
        const wishMsg = `${greeting} ${userName}, Welcome! How can I help you today?`;
        $('#WishMessage').text(wishMsg);
    }
    
    // Try to get user name
    setTimeout(getUserName, 1000);
    
    // Expose function for Python to call after face authentication
    eel.expose(updateUserAfterAuth, 'updateUserAfterAuth');
    
    // Load AI configuration
    function loadAIConfig() {
        eel.readConfigFiles()(function(configs) {
            if (configs.ai_config) {
                $('#currentAI').text(configs.ai_config.provider || 'GROQ');
            }
            if (configs.voice_config) {
                $('#currentVoice').text(configs.voice_config.gender === 'female' ? 'Female' : 'Male');
            }
            if (configs.language) {
                $('#currentLang').text(configs.language.charAt(0).toUpperCase() + configs.language.slice(1));
            }
        });
    }
    
    // Load config on startup and refresh every 10 seconds
    setTimeout(loadAIConfig, 500);
    setInterval(loadAIConfig, 10000);
    
    // Load conversation from chat canvas
    function loadConversationHistory() {
        const chatMessages = $('#chat-canvas-body .receiver_message, #chat-canvas-body .sender_message');
        const preview = $('#conversationPreview');
        
        if (chatMessages.length > 0) {
            preview.empty();
            
            // Get last 2 messages
            const lastMessages = chatMessages.slice(-2);
            lastMessages.each(function() {
                const messageText = $(this).text().trim();
                const isUser = $(this).hasClass('sender_message');
                
                if (messageText) {
                    preview.append(`
                        <div class="chat-message">
                            <div class="message-text">${messageText}</div>
                            <div class="message-time">${isUser ? 'USER' : 'JARVIS'}</div>
                        </div>
                    `);
                }
            });
        }
    }
    
    setTimeout(loadConversationHistory, 2000);
    setInterval(loadConversationHistory, 3000);
    
    // Clear chat functionality
    $('#clearChatBtn').click(function() {
        $('#chat-canvas-body').empty();
        $('#conversationPreview').empty();
        $('#conversationPreview').append('<div class="chat-message"><div class="message-text">Chat cleared</div><div class="message-time">SYSTEM</div></div>');
    });
    
    // Export chat functionality
    $('#extractChatBtn').click(function() {
        const chatMessages = $('#chat-canvas-body .receiver_message, #chat-canvas-body .sender_message');
        let chatText = 'JARVIS Chat Export\n\n';
        
        chatMessages.each(function() {
            const messageText = $(this).text().trim();
            const isUser = $(this).hasClass('sender_message');
            const sender = isUser ? 'USER' : 'JARVIS';
            chatText += `${sender}: ${messageText}\n`;
        });
        
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'jarvis_chat_export.txt';
        a.click();
        URL.revokeObjectURL(url);
    });
    
    // Network speed monitoring
    function measureNetworkSpeed() {
        eel.getNetworkSpeed()(function(speed) {
            $('#networkSpeed').text(speed + ' Mbps');
        });
    }
    
    setTimeout(measureNetworkSpeed, 3000);
    setInterval(measureNetworkSpeed, 30000);
    
    // Left panel toggle (controls both panels)
    $('#leftPanelToggle').click(function() {
        const leftCollapsed = $('#leftPanel').hasClass('collapsed');
        const rightCollapsed = $('#rightPanel').hasClass('collapsed');
        
        if (!leftCollapsed || !rightCollapsed) {
            // Hide both panels
            $('#leftPanel').addClass('collapsed');
            $('#rightPanel').addClass('collapsed');
            $('#collapsedLine').show();
        } else {
            // Show both panels
            $('#leftPanel').removeClass('collapsed');
            $('#rightPanel').removeClass('collapsed');
            $('#collapsedLine').hide();
        }
    });
    
    // Collapsed left line click to reopen both panels
    $('#collapsedLine').click(function() {
        $('#leftPanel').removeClass('collapsed');
        $('#rightPanel').removeClass('collapsed');
        $('#collapsedLine').hide();
    });
    
    // Load today's calendar events
    function loadTodaysEvents() {
        const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
        
        // Use eel to read the calendar JSON file
        eel.readCalendarEvents()(function(events) {
            const eventsContainer = $('#eventsContainer');
            const noEventsDiv = $('#noEvents');
            
            if (events && events.length > 0) {
                // Filter events for today
                const todaysEvents = events.filter(event => event.date === today);
                
                if (todaysEvents.length > 0) {
                    noEventsDiv.hide();
                    eventsContainer.empty();
                    
                    // Sort events by time
                    todaysEvents.sort((a, b) => a.time.localeCompare(b.time));
                    
                    todaysEvents.forEach(event => {
                        const eventHtml = `
                            <div class="chat-message">
                                <div class="message-text">${event.title}</div>
                                <div class="message-time">${formatTime(event.time)}</div>
                            </div>
                        `;
                        eventsContainer.append(eventHtml);
                    });
                } else {
                    eventsContainer.empty();
                    eventsContainer.append(noEventsDiv.show());
                }
            } else {
                eventsContainer.empty();
                eventsContainer.append(noEventsDiv.show());
            }
        });
    }
    
    // Format time from 24-hour to 12-hour format
    function formatTime(time24) {
        const [hours, minutes] = time24.split(':');
        const hour12 = hours % 12 || 12;
        const ampm = hours >= 12 ? 'PM' : 'AM';
        return `${hour12}:${minutes} ${ampm}`;
    }
    
    // Load reminders
    function loadReminders() {
        eel.readReminders()(function(reminders) {
            const remindersContainer = $('#remindersContainer');
            const noRemindersDiv = $('#noReminders');
            
            if (reminders && reminders.length > 0) {
                noRemindersDiv.hide();
                remindersContainer.empty();
                
                reminders.forEach(reminder => {
                    const reminderHtml = `
                        <div class="chat-message">
                            <div class="message-text">${reminder.task}</div>
                            <div class="message-time">${formatReminderTime(reminder.reminder_time)}</div>
                        </div>
                    `;
                    remindersContainer.append(reminderHtml);
                });
            } else {
                remindersContainer.empty();
                remindersContainer.append(noRemindersDiv.show());
            }
        });
    }
    
    // Format reminder time
    function formatReminderTime(timeStr) {
        const date = new Date(timeStr);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
    
    // Load events and reminders on startup and refresh every 5 minutes
    setTimeout(loadTodaysEvents, 1000);
    setTimeout(loadReminders, 1200);
    setInterval(loadTodaysEvents, 300000);
    setInterval(loadReminders, 300000);

});