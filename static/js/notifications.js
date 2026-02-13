// Professional Notification System for StockPro AI

class NotificationManager {
    constructor() {
        this.container = null;
        this.init();
    }
    
    init() {
        // Create notification container if not exists
        if (!document.getElementById('notification-container')) {
            this.container = document.createElement('div');
            this.container.id = 'notification-container';
            this.container.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 10001;
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(this.container);
        } else {
            this.container = document.getElementById('notification-container');
        }
    }
    
    show(message, type = 'info', duration = 4000) {
        const notification = document.createElement('div');
        const id = 'notif-' + Date.now();
        notification.id = id;
        
        // Get icon and colors based on type
        const config = this.getConfig(type);
        
        notification.style.cssText = `
            background: ${config.bg};
            color: ${config.text};
            padding: 16px 20px;
            border-radius: 12px;
            border-left: 4px solid ${config.border};
            box-shadow: 0 8px 32px ${config.shadow};
            display: flex;
            align-items: start;
            gap: 12px;
            min-width: 320px;
            max-width: 400px;
            pointer-events: all;
            animation: slideInRight 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        `;
        
        notification.innerHTML = `
            <div style="font-size: 1.5rem; line-height: 1;">${config.icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 4px;">${config.title}</div>
                <div style="font-size: 0.85rem; opacity: 0.9; line-height: 1.4;">${message}</div>
            </div>
            <button onclick="removeNotification('${id}')" style="
                background: none;
                border: none;
                color: ${config.text};
                cursor: pointer;
                opacity: 0.6;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
                transition: all 0.2s;
            " onmouseover="this.style.opacity='1'; this.style.background='rgba(0,0,0,0.1)'" onmouseout="this.style.opacity='0.6'; this.style.background='none'">
                <i class="bi bi-x-lg" style="font-size: 0.9rem;"></i>
            </button>
        `;
        
        this.container.appendChild(notification);
        
        // Auto remove after duration
        if (duration > 0) {
            setTimeout(() => {
                this.remove(id);
            }, duration);
        }
        
        return id;
    }
    
    remove(id) {
        const notification = document.getElementById(id);
        if (notification) {
            notification.style.animation = 'slideOutRight 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }
    
    getConfig(type) {
        const configs = {
            success: {
                icon: '<i class="bi bi-check-circle-fill"></i>',
                title: currentLang === 'id' ? 'Berhasil!' : 'Success!',
                bg: 'linear-gradient(135deg, rgba(16, 185, 129, 0.95) 0%, rgba(5, 150, 105, 0.95) 100%)',
                text: '#ffffff',
                border: '#10b981',
                shadow: 'rgba(16, 185, 129, 0.3)'
            },
            error: {
                icon: '<i class="bi bi-exclamation-circle-fill"></i>',
                title: currentLang === 'id' ? 'Terjadi Kesalahan' : 'Error Occurred',
                bg: 'linear-gradient(135deg, rgba(239, 68, 68, 0.95) 0%, rgba(220, 38, 38, 0.95) 100%)',
                text: '#ffffff',
                border: '#ef4444',
                shadow: 'rgba(239, 68, 68, 0.3)'
            },
            warning: {
                icon: '<i class="bi bi-exclamation-triangle-fill"></i>',
                title: currentLang === 'id' ? 'Peringatan' : 'Warning',
                bg: 'linear-gradient(135deg, rgba(245, 158, 11, 0.95) 0%, rgba(217, 119, 6, 0.95) 100%)',
                text: '#ffffff',
                border: '#f59e0b',
                shadow: 'rgba(245, 158, 11, 0.3)'
            },
            info: {
                icon: '<i class="bi bi-info-circle-fill"></i>',
                title: currentLang === 'id' ? 'Informasi' : 'Information',
                bg: 'linear-gradient(135deg, rgba(59, 130, 246, 0.95) 0%, rgba(37, 99, 235, 0.95) 100%)',
                text: '#ffffff',
                border: '#3b82f6',
                shadow: 'rgba(59, 130, 246, 0.3)'
            }
        };
        
        return configs[type] || configs.info;
    }
}

// Initialize notification manager
const notificationManager = new NotificationManager();

// Global functions for easy access
function showNotification(message, type = 'info', duration = 4000) {
    return notificationManager.show(message, type, duration);
}

function removeNotification(id) {
    notificationManager.remove(id);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @media (max-width: 768px) {
        #notification-container {
            top: 70px !important;
            right: 12px !important;
            left: 12px !important;
            max-width: none !important;
        }
        
        #notification-container > div {
            min-width: auto !important;
            max-width: none !important;
        }
    }
`;
document.head.appendChild(style);
