document.addEventListener('DOMContentLoaded', () => {

    const chatContainer = document.getElementById('chat-container');
    const welcomeScreen = document.getElementById('welcome-screen');
    const inputForm = document.getElementById('input-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-video-btn');
    let isVideoLoaded = false;
    let isLoading = false;

    inputForm.addEventListener('submit', handleFormSubmit);
    clearButton.addEventListener('click', handleClearVideo);

    async function handleFormSubmit(e) {
        e.preventDefault();
        if (isLoading) return;

        const text = messageInput.value.trim();
        if (text === "") return;

        messageInput.value = "";
        isLoading = true;
        toggleInput(false);

        if (isVideoLoaded) {
            addChatMessage(text, 'user');
            const loadingBubble = addLoadingBubble();
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: text })
                });
                
                chatContainer.removeChild(loadingBubble);
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to get answer.');
                }
                
                const data = await response.json();
                addChatMessage(data.answer, 'bot');
                
            } catch (err) {
                addChatMessage(`Error: ${err.message}`, 'bot-error');
            }

        } else {

            welcomeScreen.classList.add('hidden');
            chatContainer.classList.remove('hidden');

            const loadingBubble = addLoadingBubble();
            
            try {
                const response = await fetch('/load_video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ video_url: text })
                });
                
                chatContainer.removeChild(loadingBubble);
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to load video.');
                }
                
                const data = await response.json();
                if (data.status === 'success') {
                    isVideoLoaded = true;
                    
                    chatContainer.innerHTML = ''; 
                    
                    showVideoInfoBar(data.video_info);
                    messageInput.placeholder = "Ask a question about the video...";
                    clearButton.classList.remove('hidden');
                } else {
                    throw new Error(data.message);
                }
                
            } catch (err) {
                chatContainer.innerHTML = ''; 
                chatContainer.classList.add('hidden'); 
                welcomeScreen.classList.remove('hidden'); 
                alert(`Error: ${err.message}`);
            }
        }
        
        isLoading = false;
        toggleInput(true);
        messageInput.focus();
    }
    
    async function handleClearVideo() {
        if (isLoading) return;

        try {
            await fetch('/clear', { method: 'POST' });
        } catch (err) {
            console.error('Failed to clear server cache:', err);
        }

        isVideoLoaded = false;

        chatContainer.innerHTML = ''; 
        chatContainer.classList.add('hidden'); 
        welcomeScreen.classList.remove('hidden'); 

        hideVideoInfoBar(); 
        messageInput.placeholder = "Enter a YouTube URL...";
        clearButton.classList.add('hidden');

    }

    
    function addChatMessage(message, type) {
        const bubble = document.createElement('div');
        bubble.classList.add('chat-bubble');

        if (type === 'user') {
            bubble.classList.add('user-bubble');
            bubble.textContent = message;
        } else if (type === 'bot') {
            bubble.classList.add('bot-bubble');
            bubble.textContent = message;
        } else if (type === 'user-info') {

            bubble.classList.add('info-bubble', 'text-sm', 'text-center');
            bubble.textContent = message;
        } else if (type === 'bot-error') {
            bubble.classList.add('bot-bubble', 'text-red-600', 'border-red-200');
            bubble.textContent = message;
        }
        
        chatContainer.appendChild(bubble);
        scrollToBottom();
        return bubble;
    }
    
    function showVideoInfoBar(info) {
        const bar = document.getElementById('video-info-bar');
        const img = document.getElementById('video-info-img');
        const status = document.getElementById('video-info-status');
        const title = document.getElementById('video-info-title');
        const channel = document.getElementById('video-info-channel');

        img.src = info.thumbnail_url.replace('default.jpg', 'hqdefault.jpg');

        title.textContent = info.title;
        channel.textContent = info.channel;

        if (info.title === 'Unknown Title') {
            status.textContent = 'Transcript loaded (metadata failed).';
            status.classList.remove('text-green-600');
            status.classList.add('text-amber-600');
            title.textContent = 'Unknown Title';
            channel.textContent = 'Unknown Channel';
        } else {
            status.textContent = 'Video Loaded:';
            status.classList.remove('text-amber-600');
            status.classList.add('text-green-600');
        }

        bar.classList.remove('hidden');

        addChatMessage("You can now ask questions about this video.", 'bot');
    }


    function hideVideoInfoBar() {
        const bar = document.getElementById('video-info-bar');
        bar.classList.add('hidden');

        document.getElementById('video-info-img').src = "";
        document.getElementById('video-info-title').textContent = "";
        document.getElementById('video-info-channel').textContent = "";
    }

    function addLoadingBubble() {
        const bubble = document.createElement('div');
        bubble.classList.add(
            'chat-bubble', 'loading-bubble', 
            'flex', 'space-x-1', 'items-center'
        );
        
        bubble.innerHTML = `
            <span class="font-medium">Thinking</span>
            <div class="w-2 h-2 bg-gray-500 rounded-full loading-dot"></div>
            <div class="w-2 h-2 bg-gray-500 rounded-full loading-dot"></div>
            <div class="w-2 h-2 bg-gray-500 rounded-full loading-dot"></div>
        `;
        
        chatContainer.appendChild(bubble);
        scrollToBottom();
        return bubble;
    }

    function toggleInput(enabled) {
        messageInput.disabled = !enabled;
        sendButton.disabled = !enabled;
        sendButton.classList.toggle('opacity-50', !enabled);
        sendButton.classList.toggle('cursor-not-allowed', !enabled);
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    const watermarkButton = document.getElementById('watermark-button');
const modal = document.getElementById('developer-modal');
const modalCloseButton = document.getElementById('modal-close-btn');

if (watermarkButton && modal && modalCloseButton) {

    const openModal = () => {
        modal.classList.remove('hidden');
        modal.style.opacity = '0';
        const modalWindow = modal.querySelector('.modal-window');

        modalWindow.style.animation = 'none';
        void modalWindow.offsetWidth; 
        modalWindow.style.animation = 'modalPopIn 0.2s ease-out';
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10); 
    };

    const closeModal = () => {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 200); 
    };

    watermarkButton.addEventListener('click', openModal);

    modalCloseButton.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}
});

