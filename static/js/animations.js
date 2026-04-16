/**
 * AWS Learning Platform - Advanced Animations & Interactivity
 * For engaging student education with visual effects
 */

// ===== ANIMATED BACKGROUND PARTICLES =====
function createBackgroundParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;
    document.body.appendChild(particleContainer);

    // Create 20 floating particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 8 + 4}px;
            height: ${Math.random() * 8 + 4}px;
            background: rgba(255, 153, 0, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: particleFloat ${Math.random() * 10 + 15}s linear infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particleContainer.appendChild(particle);
    }
}

// ===== ANIMATED COUNTER (for stats) =====
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// ===== LEVEL UP CELEBRATION =====
function celebrateLevelUp(newLevel) {
    // Create modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;

    const content = document.createElement('div');
    content.style.cssText = `
        background: linear-gradient(135deg, #FF9900, #146EB4);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        animation: levelUpCelebration 1s ease-out;
    `;
    content.innerHTML = `
        <div style="font-size: 5rem; animation: bounce 1s ease-in-out infinite;">🎉</div>
        <h1 style="font-size: 3rem; margin: 1rem 0;">LEVEL UP!</h1>
        <p style="font-size: 2rem; font-weight: bold;">Level ${newLevel}</p>
        <p style="font-size: 1.2rem; margin-top: 1rem;">You're on fire! Keep learning!</p>
    `;

    modal.appendChild(content);
    document.body.appendChild(modal);

    // Create confetti
    createConfetti();

    // Play sound (if available)
    playSound('levelup');

    // Remove after 3 seconds
    setTimeout(() => {
        modal.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => modal.remove(), 300);
    }, 3000);
}

// ===== CONFETTI EFFECT =====
function createConfetti() {
    const colors = ['#FF9900', '#146EB4', '#3FB618', '#7B42BC', '#D13212'];
    const confettiCount = 100;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: ${Math.random() * 10 + 5}px;
            height: ${Math.random() * 10 + 5}px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${Math.random() * 100}%;
            top: -20px;
            opacity: ${Math.random() * 0.5 + 0.5};
            animation: confetti-fall ${Math.random() * 3 + 2}s linear;
            z-index: 10001;
            border-radius: ${Math.random() > 0.5 ? '50%' : '0'};
        `;
        document.body.appendChild(confetti);

        // Remove after animation
        setTimeout(() => confetti.remove(), 5000);
    }
}

// ===== BADGE UNLOCK ANIMATION =====
function showBadgeUnlock(badgeName, badgeIcon) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: -400px;
        background: linear-gradient(135deg, #232F3E, #146EB4);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideInFromRight 0.5s ease forwards;
    `;
    notification.innerHTML = `
        <div style="font-size: 3rem; animation: bounce 1s ease-in-out infinite;">${badgeIcon}</div>
        <div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Badge Unlocked!</div>
            <div style="font-size: 1.3rem; font-weight: bold;">${badgeName}</div>
        </div>
    `;
    document.body.appendChild(notification);

    // Slide in
    setTimeout(() => {
        notification.style.right = '20px';
    }, 100);

    // Slide out
    setTimeout(() => {
        notification.style.animation = 'slideOutToRight 0.5s ease forwards';
        setTimeout(() => notification.remove(), 500);
    }, 4000);

    // Play sound
    playSound('badge');
}

// ===== PROGRESS BAR ANIMATION =====
function animateProgressBar(progressBar, percentage) {
    const fill = progressBar.querySelector('.progress-fill');
    if (fill) {
        setTimeout(() => {
            fill.style.width = percentage + '%';
        }, 100);
    }
}

// ===== SOUND EFFECTS =====
function playSound(type) {
    // Create AudioContext for simple sound effects
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        if (type === 'levelup') {
            // Ascending chord
            oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5
            oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // E5
            oscillator.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2); // G5
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } else if (type === 'badge') {
            // Single note
            oscillator.frequency.value = 800;
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        } else if (type === 'click') {
            // Click sound
            oscillator.frequency.value = 1000;
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.05);
        }
    } catch (error) {
        // Silently fail if audio not supported
        console.log('Audio not supported');
    }
}

// ===== ANIMATED CARD ENTRANCE =====
function animateCardsOnScroll() {
    const cards = document.querySelectorAll('.lesson-card, .stat-box');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });
}

// ===== 3D CARD TILT EFFECT (follows mouse) =====
function enable3DCardTilt() {
    const cards = document.querySelectorAll('.lesson-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `
                perspective(1000px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                translateY(-10px)
                scale(1.02)
            `;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
        });
    });
}

// ===== INTERACTIVE AWS SERVICE DIAGRAM =====
function createAWSArchitectureDiagram(containerId, services) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '400');
    svg.style.cssText = 'background: #f8f9fa; border-radius: 10px;';

    // Example: User -> API Gateway -> Lambda -> DynamoDB
    const nodes = services || [
        { id: 'user', x: 50, y: 200, label: 'User', icon: '👤', color: '#232F3E' },
        { id: 'api', x: 200, y: 200, label: 'API Gateway', icon: '🚪', color: '#FF9900' },
        { id: 'lambda', x: 350, y: 200, label: 'Lambda', icon: '⚡', color: '#146EB4' },
        { id: 'db', x: 500, y: 200, label: 'Database', icon: '💾', color: '#3FB618' }
    ];

    // Draw connections
    for (let i = 0; i < nodes.length - 1; i++) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', nodes[i].x + 40);
        line.setAttribute('y1', nodes[i].y);
        line.setAttribute('x2', nodes[i + 1].x - 40);
        line.setAttribute('y2', nodes[i + 1].y);
        line.setAttribute('stroke', '#146EB4');
        line.setAttribute('stroke-width', '3');
        line.setAttribute('stroke-dasharray', '10,5');
        line.style.animation = `dashAnimation 2s linear infinite`;
        svg.appendChild(line);
    }

    // Draw nodes
    nodes.forEach((node, index) => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'diagram-node');
        g.style.cursor = 'pointer';
        g.style.animation = `fadeIn 0.5s ease ${index * 0.2}s both`;

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', node.x);
        circle.setAttribute('cy', node.y);
        circle.setAttribute('r', '35');
        circle.setAttribute('fill', node.color);
        circle.setAttribute('stroke', 'white');
        circle.setAttribute('stroke-width', '3');

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', node.x);
        text.setAttribute('y', node.y + 5);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', 'white');
        text.setAttribute('font-size', '24');
        text.textContent = node.icon;

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', node.x);
        label.setAttribute('y', node.y + 55);
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('font-size', '14');
        label.setAttribute('font-weight', 'bold');
        label.textContent = node.label;

        g.appendChild(circle);
        g.appendChild(text);
        g.appendChild(label);
        svg.appendChild(g);

        // Hover effect
        g.addEventListener('mouseenter', () => {
            circle.setAttribute('r', '45');
            circle.style.filter = 'drop-shadow(0 0 20px rgba(255,153,0,0.8))';
        });
        g.addEventListener('mouseleave', () => {
            circle.setAttribute('r', '35');
            circle.style.filter = 'none';
        });
    });

    container.appendChild(svg);
}

// Add CSS for diagram animation
const style = document.createElement('style');
style.textContent = `
    @keyframes dashAnimation {
        to { stroke-dashoffset: -30; }
    }
    @keyframes slideOutToRight {
        to { transform: translateX(500px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// ===== TOOLTIP SYSTEM =====
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');

        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = tooltipText;
            tooltip.style.cssText = `
                position: fixed;
                background: #232F3E;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.9rem;
                z-index: 10000;
                pointer-events: none;
                animation: fadeIn 0.2s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            `;
            document.body.appendChild(tooltip);

            const updatePosition = (event) => {
                tooltip.style.left = (event.clientX + 10) + 'px';
                tooltip.style.top = (event.clientY + 10) + 'px';
            };

            updatePosition(e);
            element.addEventListener('mousemove', updatePosition);

            element.addEventListener('mouseleave', () => {
                tooltip.remove();
                element.removeEventListener('mousemove', updatePosition);
            }, { once: true });
        });
    });
}

// ===== INITIALIZE ALL ANIMATIONS =====
function initializeAnimations() {
    // Wait for DOM to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        createBackgroundParticles();
        animateCardsOnScroll();
        enable3DCardTilt();
        initTooltips();

        // Animate stat counters
        document.querySelectorAll('.counter').forEach(counter => {
            const target = parseInt(counter.textContent);
            if (!isNaN(target)) {
                animateCounter(counter, target);
            }
        });

        // Animate progress bars
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const fill = bar.querySelector('.progress-fill');
            if (fill) {
                const width = fill.style.width;
                fill.style.width = '0%';
                setTimeout(() => {
                    fill.style.width = width;
                }, 500);
            }
        });

        // Add click sound to all buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', () => playSound('click'));
        });
    }
}

// Auto-initialize
initializeAnimations();

// Export functions for use in other scripts
window.AWSAnimations = {
    celebrateLevelUp,
    showBadgeUnlock,
    createConfetti,
    createAWSArchitectureDiagram,
    animateProgressBar,
    playSound
};
