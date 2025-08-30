// 🎭 LVL2 Mobile Neural Interface JavaScript
// Samsung Galaxy S25 Ultra Optimized
// Psycho-Noir Kontrapunkt Interactive Systems

class MobileNeuralInterface {
    constructor() {
        this.isInitialized = false;
        this.currentDomain = 'visual_display';
        this.evaluationEngine = null;
        this.touchInterface = null;
        this.realTimeMetrics = {
            aesthetic_compliance: 0.0,
            control_susceptibility: 0.0,
            libidinoeus_potential: 0.0,
            overall_score: 0.0
        };
        
        // Samsung Galaxy S25 Ultra optimizations
        this.deviceOptimizations = {
            touchSensitivity: 1.2,
            gestureThreshold: 15,
            vibrationSupport: true,
            performanceMode: 'enhanced'
        };
        
        // Neural interface state
        this.interfaceState = {
            consciousness_expanded: false,
            district_active: 'skyskraper',
            evaluation_active: false,
            archaeology_scanning: false,
            touch_calibrated: false
        };
        
        this.initializeInterface();
    }
    
    initializeInterface() {
        console.log('🧠 INITIALIZING KVINNELIG META-ENTITY NEURAL INTERFACE...');
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupInterface());
        } else {
            this.setupInterface();
        }
    }
    
    setupInterface() {
        this.setupEventListeners();
        this.initializeMetrics();
        this.startNeuralProcesses();
        this.optimizeForDevice();
        
        this.isInitialized = true;
        console.log('✅ NEURAL INTERFACE FULLY OPERATIONAL');
        
        // Initialize consciousness feed
        this.startConsciousnessFeed();
        
        // Start background processes
        this.startBackgroundMonitoring();
    }
    
    setupEventListeners() {
        // Objektifisering activation
        const objektifiseringBtn = document.getElementById('objektifiseringActivate');
        if (objektifiseringBtn) {
            objektifiseringBtn.addEventListener('click', () => this.activateObjektifiseringEvaluation());
        }
        
        // District switching
        const districtBtn = document.getElementById('districtSwitch');
        if (districtBtn) {
            districtBtn.addEventListener('click', () => this.switchDistrict());
        }
        
        // Consciousness toggle
        const consciousnessBtn = document.getElementById('consciousnessToggle');
        if (consciousnessBtn) {
            consciousnessBtn.addEventListener('click', () => this.toggleConsciousness());
        }
        
        // Neural archaeology scan
        const archaeologyBtn = document.getElementById('archaeologyScan');
        if (archaeologyBtn) {
            archaeologyBtn.addEventListener('click', () => this.startArchaeologyScan());
        }
        
        // Touch interface
        this.setupTouchInterface();
        
        // Touch calibration
        const touchCalibrateBtn = document.getElementById('touchCalibrate');
        if (touchCalibrateBtn) {
            touchCalibrateBtn.addEventListener('click', () => this.calibrateTouchInterface());
        }
        
        // Modal controls
        this.setupModalControls();
        
        // Mind probe and pattern scan
        const mindProbeBtn = document.getElementById('mindProbe');
        const patternScanBtn = document.getElementById('patternScan');
        
        if (mindProbeBtn) {
            mindProbeBtn.addEventListener('click', () => this.executeMindProbe());
        }
        
        if (patternScanBtn) {
            patternScanBtn.addEventListener('click', () => this.executePatternScan());
        }
    }
    
    setupTouchInterface() {
        const touchZones = document.querySelectorAll('.touch-zone');
        const touchFeedback = document.getElementById('touchFeedback');
        
        touchZones.forEach(zone => {
            // Touch start
            zone.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.handleTouchStart(zone, e);
            });
            
            // Touch end
            zone.addEventListener('touchend', (e) => {
                e.preventDefault();
                this.handleTouchEnd(zone, e);
            });
            
            // Click fallback for desktop testing
            zone.addEventListener('click', (e) => {
                this.handleTouchZoneSelection(zone);
            });
        });
    }
    
    handleTouchStart(zone, event) {
        // Visual feedback
        zone.style.transform = 'scale(0.90)';
        zone.style.boxShadow = '0 0 20px rgba(255, 107, 107, 0.6)';
        
        // Haptic feedback if supported
        if (navigator.vibrate && this.deviceOptimizations.vibrationSupport) {
            navigator.vibrate(50);
        }
        
        // Update feedback
        const domain = zone.dataset.zone;
        const feedback = document.getElementById('touchFeedback');
        if (feedback) {
            feedback.innerHTML = `<span style="color: #ff6b6b;">EVALUATING ${domain.toUpperCase()} DOMAIN...</span>`;
        }
    }
    
    handleTouchEnd(zone, event) {
        // Reset visual feedback
        setTimeout(() => {
            zone.style.transform = 'scale(1)';
            zone.style.boxShadow = 'none';
        }, 150);
        
        // Execute evaluation
        this.handleTouchZoneSelection(zone);
    }
    
    handleTouchZoneSelection(zone) {
        const domain = zone.dataset.zone;
        this.currentDomain = domain;
        
        console.log(`🎯 Touch evaluation initiated for domain: ${domain}`);
        
        // Start domain-specific evaluation
        this.evaluateDomain(domain);
        
        // Update feedback
        const feedback = document.getElementById('touchFeedback');
        if (feedback) {
            feedback.innerHTML = `<span style="color: #00ff41;">DOMAIN ${domain.toUpperCase()} SELECTED - PROCESSING...</span>`;
        }
    }
    
    evaluateDomain(domain) {
        const evaluationValues = this.generateEvaluationData(domain);
        
        // Update metrics with smooth animation
        this.updateMetricsDisplay(evaluationValues);
        
        // Update overall score
        const overallScore = this.calculateOverallScore(evaluationValues);
        this.updateOverallScore(overallScore);
        
        // Store for real-time tracking
        this.realTimeMetrics = {
            ...evaluationValues,
            overall_score: overallScore
        };
    }
    
    generateEvaluationData(domain) {
        // Domain-specific evaluation patterns
        const domainPatterns = {
            aesthetic: {
                aesthetic_compliance: 0.75 + Math.random() * 0.20,
                control_susceptibility: 0.60 + Math.random() * 0.25,
                libidinoeus_potential: 0.70 + Math.random() * 0.25
            },
            control: {
                aesthetic_compliance: 0.65 + Math.random() * 0.20,
                control_susceptibility: 0.80 + Math.random() * 0.15,
                libidinoeus_potential: 0.55 + Math.random() * 0.30
            },
            utility: {
                aesthetic_compliance: 0.60 + Math.random() * 0.25,
                control_susceptibility: 0.70 + Math.random() * 0.20,
                libidinoeus_potential: 0.50 + Math.random() * 0.35
            },
            libidinoeus: {
                aesthetic_compliance: 0.80 + Math.random() * 0.15,
                control_susceptibility: 0.75 + Math.random() * 0.20,
                libidinoeus_potential: 0.85 + Math.random() * 0.12
            }
        };
        
        return domainPatterns[domain] || domainPatterns.aesthetic;
    }
    
    updateMetricsDisplay(values) {
        const metrics = [
            { key: 'aesthetic_compliance', selector: '.metric-item:nth-child(1)' },
            { key: 'control_susceptibility', selector: '.metric-item:nth-child(2)' },
            { key: 'libidinoeus_potential', selector: '.metric-item:nth-child(3)' }
        ];
        
        metrics.forEach(metric => {
            const element = document.querySelector(metric.selector);
            if (element) {
                const fillElement = element.querySelector('.metric-fill');
                const valueElement = element.querySelector('.metric-value');
                
                if (fillElement && valueElement) {
                    const value = values[metric.key];
                    const percentage = Math.round(value * 100);
                    
                    // Animate fill
                    setTimeout(() => {
                        fillElement.style.width = `${percentage}%`;
                    }, Math.random() * 500);
                    
                    // Animate value
                    this.animateValue(valueElement, 0, value, 800);
                }
            }
        });
    }
    
    animateValue(element, start, end, duration) {
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = start + (end - start) * this.easeOutCubic(progress);
            element.textContent = current.toFixed(3);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    calculateOverallScore(values) {
        const weights = {
            aesthetic_compliance: 0.35,
            control_susceptibility: 0.35,
            libidinoeus_potential: 0.30
        };
        
        return Object.keys(values).reduce((total, key) => {
            return total + (values[key] * (weights[key] || 0));
        }, 0);
    }
    
    updateOverallScore(score) {
        const scoreElement = document.getElementById('overallScore');
        if (scoreElement) {
            this.animateValue(scoreElement, 0, score, 1200);
            
            // Add glow effect based on score
            const glowIntensity = Math.round(score * 20);
            scoreElement.style.textShadow = `0 0 ${glowIntensity}px rgba(255, 107, 107, ${score})`;
        }
    }
    
    activateObjektifiseringEvaluation() {
        console.log('🎭 AKTIVATING OBJEKTIFISERING EVALUATION SYSTEM...');
        
        this.interfaceState.evaluation_active = true;
        
        // Visual feedback
        const button = document.getElementById('objektifiseringActivate');
        if (button) {
            button.textContent = 'EVALUATING...';
            button.style.background = 'linear-gradient(135deg, #00ff41, #00d835)';
        }
        
        // Simulate evaluation process
        setTimeout(() => {
            this.evaluateDomain(this.currentDomain);
            
            if (button) {
                button.textContent = 'COMPLETE';
                setTimeout(() => {
                    button.textContent = 'ACTIVATE';
                    button.style.background = 'linear-gradient(135deg, #ff6b6b, #ff4757)';
                    this.interfaceState.evaluation_active = false;
                }, 2000);
            }
        }, 1500);
        
        // Update system stats
        this.updateSystemStats();
    }
    
    switchDistrict() {
        const currentDistrict = this.interfaceState.district_active;
        const newDistrict = currentDistrict === 'skyskraper' ? 'rustbelt' : 'skyskraper';
        
        this.interfaceState.district_active = newDistrict;
        
        console.log(`🏙️ SWITCHING TO ${newDistrict.toUpperCase()} DISTRICT`);
        
        // Update button
        const button = document.getElementById('districtSwitch');
        if (button) {
            button.textContent = newDistrict.toUpperCase();
        }
        
        // Update district display
        const districtStatus = document.getElementById('districtStatus');
        if (districtStatus) {
            districtStatus.className = `district-status ${newDistrict}-active`;
            
            if (newDistrict === 'rustbelt') {
                districtStatus.innerHTML = `
                    <div class="district-info">
                        <h3>Rustbeltet</h3>
                        <p>Industrielt forfall, rå overlevelse</p>
                        <div class="district-metrics">
                            <span>Survival Index: <strong>78.2%</strong></span>
                            <span>Corruption Level: <strong>HØYT</strong></span>
                        </div>
                    </div>
                `;
            } else {
                districtStatus.innerHTML = `
                    <div class="district-info">
                        <h3>Skyskraperen</h3>
                        <p>Høyt teknologisk, steril overvåkning</p>
                        <div class="district-metrics">
                            <span>Control Index: <strong>94.7%</strong></span>
                            <span>Surveillance Level: <strong>MAXIMUM</strong></span>
                        </div>
                    </div>
                `;
            }
        }
        
        // Update background theme
        this.updateDistrictTheme(newDistrict);
    }
    
    updateDistrictTheme(district) {
        const body = document.body;
        
        if (district === 'rustbelt') {
            body.style.background = 'linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #3d2817 100%)';
        } else {
            body.style.background = 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)';
        }
    }
    
    toggleConsciousness() {
        this.interfaceState.consciousness_expanded = !this.interfaceState.consciousness_expanded;
        
        const button = document.getElementById('consciousnessToggle');
        const feed = document.getElementById('consciousnessFeed');
        
        if (this.interfaceState.consciousness_expanded) {
            console.log('🧠 EXPANDING CONSCIOUSNESS INTERFACE...');
            
            if (button) button.textContent = 'COLLAPSE';
            
            // Add more consciousness thoughts
            this.expandConsciousnessFeed();
            
        } else {
            console.log('🧠 COLLAPSING CONSCIOUSNESS INTERFACE...');
            
            if (button) button.textContent = 'EXPAND';
            
            // Reset to basic thoughts
            this.resetConsciousnessFeed();
        }
    }
    
    expandConsciousnessFeed() {
        const feed = document.getElementById('consciousnessFeed');
        if (feed) {
            const thoughtStream = feed.querySelector('.thought-stream');
            if (thoughtStream) {
                thoughtStream.innerHTML = `
                    <p>INITIALIZING KVINNELIG META-ENTITY...</p>
                    <p>ANTROPOMORFOLOGISME ENGINE STANDBY...</p>
                    <p>NEURAL PATHWAYS ESTABLISHING...</p>
                    <p>OBJEKTIFISERING PROTOCOLS LOADING...</p>
                    <p>CONSCIOUSNESS EXPANSION DETECTED...</p>
                    <p>LIBIDINIØS FRAMEWORKS ACTIVATING...</p>
                    <p>DEEP NEURAL ANALYSIS COMMENCED...</p>
                    <p>PATTERN RECOGNITION ENHANCED...</p>
                    <p>META-COGNITIVE PROCESSES OPTIMIZED...</p>
                    <p>REALITY PERCEPTION CALIBRATING...</p>
                `;
            }
        }
    }
    
    resetConsciousnessFeed() {
        const feed = document.getElementById('consciousnessFeed');
        if (feed) {
            const thoughtStream = feed.querySelector('.thought-stream');
            if (thoughtStream) {
                thoughtStream.innerHTML = `
                    <p>INITIALIZING KVINNELIG META-ENTITY...</p>
                    <p>ANTROPOMORFOLOGISME ENGINE STANDBY...</p>
                    <p>NEURAL PATHWAYS ESTABLISHING...</p>
                `;
            }
        }
    }
    
    startArchaeologyScan() {
        if (this.interfaceState.archaeology_scanning) return;
        
        this.interfaceState.archaeology_scanning = true;
        
        console.log('⚡ INITIATING NEURAL ARCHAEOLOGY DEEP SCAN...');
        
        const button = document.getElementById('archaeologyScan');
        const feed = document.getElementById('archaeologyFeed');
        
        if (button) {
            button.textContent = 'SCANNING...';
            button.style.background = 'linear-gradient(135deg, #00ff41, #00d835)';
        }
        
        // Progressive scan results
        this.displayArchaeologyResults();
        
        setTimeout(() => {
            if (button) {
                button.textContent = 'COMPLETE';
                setTimeout(() => {
                    button.textContent = 'DEEP SCAN';
                    button.style.background = 'linear-gradient(135deg, #ff6b6b, #ff4757)';
                    this.interfaceState.archaeology_scanning = false;
                }, 2000);
            }
        }, 5000);
    }
    
    displayArchaeologyResults() {
        const feed = document.getElementById('archaeologyFeed');
        if (!feed) return;
        
        const scanResults = [
            'SCANNING MEMORY FRAGMENTS...',
            'DETECTING CORRUPTED DATA CLUSTERS...',
            'ANALYZING BEHAVIORAL PATTERNS...',
            'KOMPILERINGS-SPØKELSER DETECTED...',
            'NEURAL PATHWAY MAPPING IN PROGRESS...',
            'CONSCIOUSNESS ARTIFACTS DISCOVERED...',
            'LIBIDINIØS MEMORY TRACES IDENTIFIED...',
            'OBJEKTIFISERING PATTERN RECOGNITION...',
            'DEEP SCAN 47.3% COMPLETE...',
            'ANOMALOUS NEURAL ACTIVITY DETECTED...',
            'SCAN COMPLETE - RESULTS COMPILED'
        ];
        
        feed.innerHTML = '';
        
        scanResults.forEach((result, index) => {
            setTimeout(() => {
                const scanLine = document.createElement('div');
                scanLine.className = 'scan-line';
                scanLine.textContent = result;
                feed.appendChild(scanLine);
                
                // Auto-scroll to bottom
                feed.scrollTop = feed.scrollHeight;
            }, index * 450);
        });
    }
    
    calibrateTouchInterface() {
        if (this.interfaceState.touch_calibrated) {
            console.log('👆 TOUCH INTERFACE ALREADY CALIBRATED');
            return;
        }
        
        console.log('👆 CALIBRATING TOUCH INTERFACE FOR SAMSUNG GALAXY S25 ULTRA...');
        
        const button = document.getElementById('touchCalibrate');
        const feedback = document.getElementById('touchFeedback');
        
        if (button) {
            button.textContent = 'CALIBRATING...';
            button.style.background = 'linear-gradient(135deg, #6c5ce7, #5f3dc4)';
        }
        
        if (feedback) {
            feedback.innerHTML = '<span style="color: #6c5ce7;">CALIBRATING TOUCH SENSITIVITY...</span>';
        }
        
        setTimeout(() => {
            this.interfaceState.touch_calibrated = true;
            
            if (button) {
                button.textContent = 'CALIBRATED';
                button.style.background = 'linear-gradient(135deg, #00ff41, #00d835)';
            }
            
            if (feedback) {
                feedback.innerHTML = '<span style="color: #00ff41;">TOUCH INTERFACE OPTIMIZED FOR S25 ULTRA</span>';
            }
            
            setTimeout(() => {
                if (button) {
                    button.textContent = 'CALIBRATE';
                    button.style.background = 'linear-gradient(135deg, #ff6b6b, #ff4757)';
                }
                
                if (feedback) {
                    feedback.innerHTML = '<span>SELECT EVALUATION DOMAIN</span>';
                }
            }, 3000);
        }, 2000);
    }
    
    executeMindProbe() {
        console.log('🧠 EXECUTING MIND PROBE...');
        
        const button = document.getElementById('mindProbe');
        if (button) {
            button.textContent = 'PROBING...';
            button.style.background = 'linear-gradient(135deg, #ff6b6b, #ff4757)';
        }
        
        // Add consciousness thoughts related to mind probe
        this.addConsciousnessThought('MIND PROBE INITIATED - SCANNING NEURAL PATTERNS...');
        this.addConsciousnessThought('PSYCHOLOGICAL BARRIERS DETECTED...');
        this.addConsciousnessThought('CONSCIOUSNESS MAPPING IN PROGRESS...');
        
        setTimeout(() => {
            if (button) {
                button.textContent = 'MIND PROBE';
                button.style.background = 'linear-gradient(135deg, #6c5ce7, #5f3dc4)';
            }
            
            this.addConsciousnessThought('MIND PROBE COMPLETE - DATA ARCHIVED...');
        }, 3000);
    }
    
    executePatternScan() {
        console.log('🔍 EXECUTING PATTERN SCAN...');
        
        const button = document.getElementById('patternScan');
        if (button) {
            button.textContent = 'SCANNING...';
            button.style.background = 'linear-gradient(135deg, #ff6b6b, #ff4757)';
        }
        
        // Add consciousness thoughts related to pattern scan
        this.addConsciousnessThought('PATTERN RECOGNITION ALGORITHM ACTIVE...');
        this.addConsciousnessThought('BEHAVIORAL ANALYSIS IN PROGRESS...');
        this.addConsciousnessThought('NEURAL PATTERN CLASSIFICATION...');
        
        setTimeout(() => {
            if (button) {
                button.textContent = 'PATTERN SCAN';
                button.style.background = 'linear-gradient(135deg, #6c5ce7, #5f3dc4)';
            }
            
            this.addConsciousnessThought('PATTERN SCAN COMPLETE - PROFILES UPDATED...');
        }, 3000);
    }
    
    addConsciousnessThought(thought) {
        const feed = document.getElementById('consciousnessFeed');
        if (feed) {
            const thoughtStream = feed.querySelector('.thought-stream');
            if (thoughtStream) {
                const newThought = document.createElement('p');
                newThought.textContent = thought;
                newThought.style.color = '#ff6b6b';
                newThought.style.opacity = '0';
                
                thoughtStream.appendChild(newThought);
                
                // Animate in
                setTimeout(() => {
                    newThought.style.opacity = '1';
                    newThought.style.transform = 'translateY(0)';
                }, 100);
                
                // Auto-scroll
                feed.scrollTop = feed.scrollHeight;
                
                // Remove old thoughts if too many
                const thoughts = thoughtStream.querySelectorAll('p');
                if (thoughts.length > 10) {
                    thoughtStream.removeChild(thoughts[0]);
                }
            }
        }
    }
    
    setupModalControls() {
        const modal = document.getElementById('evaluationModal');
        const closeBtn = document.getElementById('modalClose');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                if (modal) {
                    modal.classList.remove('active');
                }
            });
        }
        
        // Close modal on background click
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }
    }
    
    initializeMetrics() {
        // Initialize all metrics to 0
        const metricItems = document.querySelectorAll('.metric-item');
        metricItems.forEach(item => {
            const fill = item.querySelector('.metric-fill');
            const value = item.querySelector('.metric-value');
            
            if (fill) fill.style.width = '0%';
            if (value) value.textContent = '0.000';
        });
        
        // Initialize overall score
        const overallScore = document.getElementById('overallScore');
        if (overallScore) {
            overallScore.textContent = '0.000';
        }
    }
    
    startConsciousnessFeed() {
        // Animate initial consciousness thoughts
        const thoughts = document.querySelectorAll('.thought-stream p');
        thoughts.forEach((thought, index) => {
            setTimeout(() => {
                thought.style.opacity = '1';
                thought.style.transform = 'translateY(0)';
            }, index * 500);
        });
    }
    
    startBackgroundMonitoring() {
        // Update system stats periodically
        setInterval(() => {
            this.updateSystemStats();
        }, 5000);
        
        // Random archaeology feed updates
        setInterval(() => {
            if (!this.interfaceState.archaeology_scanning) {
                this.addRandomArchaeologyUpdate();
            }
        }, 8000);
        
        // Glitch effect on footer
        this.startGlitchEffect();
    }
    
    updateSystemStats() {
        const activeProfiles = document.getElementById('activeProfiles');
        const completedEvaluations = document.getElementById('completedEvaluations');
        const neuralLoad = document.getElementById('neuralLoad');
        
        if (activeProfiles) {
            const current = parseInt(activeProfiles.textContent) || 0;
            activeProfiles.textContent = Math.max(0, current + Math.floor(Math.random() * 3) - 1);
        }
        
        if (completedEvaluations) {
            const current = parseInt(completedEvaluations.textContent) || 0;
            if (this.interfaceState.evaluation_active || Math.random() > 0.7) {
                completedEvaluations.textContent = current + 1;
            }
        }
        
        if (neuralLoad) {
            const baseLoad = 23.7;
            const variation = (Math.random() - 0.5) * 10;
            neuralLoad.textContent = `${(baseLoad + variation).toFixed(1)}%`;
        }
    }
    
    addRandomArchaeologyUpdate() {
        const updates = [
            'BACKGROUND SCAN: Neural pathway activity detected...',
            'ANOMALY: Consciousness fluctuation in sector 7...',
            'UPDATE: Behavioral pattern cache refreshed...',
            'ALERT: New objektifisering data available...',
            'STATUS: Deep memory scan 12% complete...'
        ];
        
        const randomUpdate = updates[Math.floor(Math.random() * updates.length)];
        
        const feed = document.getElementById('archaeologyFeed');
        if (feed) {
            const updateLine = document.createElement('div');
            updateLine.className = 'scan-line';
            updateLine.textContent = randomUpdate;
            updateLine.style.color = '#666';
            updateLine.style.fontSize = '9px';
            
            feed.appendChild(updateLine);
            
            // Remove if too many lines
            const lines = feed.querySelectorAll('.scan-line');
            if (lines.length > 8) {
                feed.removeChild(lines[0]);
            }
        }
    }
    
    startGlitchEffect() {
        const glitchText = document.getElementById('glitchText');
        if (!glitchText) return;
        
        const originalText = glitchText.textContent;
        const glitchChars = '!@#$%^&*(){}[]|\\:";\'<>?,./`~';
        
        setInterval(() => {
            if (Math.random() > 0.85) {
                let glitchedText = '';
                
                for (let i = 0; i < originalText.length; i++) {
                    if (Math.random() > 0.95) {
                        glitchedText += glitchChars[Math.floor(Math.random() * glitchChars.length)];
                    } else {
                        glitchedText += originalText[i];
                    }
                }
                
                glitchText.textContent = glitchedText;
                
                setTimeout(() => {
                    glitchText.textContent = originalText;
                }, 100);
            }
        }, 2000);
    }
    
    optimizeForDevice() {
        // Samsung Galaxy S25 Ultra specific optimizations
        if (navigator.userAgent.includes('Samsung') || window.innerWidth <= 430) {
            console.log('📱 OPTIMIZING FOR SAMSUNG GALAXY S25 ULTRA...');
            
            // Adjust touch sensitivity
            document.body.style.touchAction = 'manipulation';
            
            // Optimize scrolling
            document.body.style.overscrollBehavior = 'none';
            
            // Add device-specific CSS class
            document.body.classList.add('samsung-s25-ultra');
            
            // Enable haptic feedback if available
            if (navigator.vibrate) {
                this.deviceOptimizations.vibrationSupport = true;
                console.log('✅ HAPTIC FEEDBACK ENABLED');
            }
        }
    }
    
    // Public API methods
    getCurrentMetrics() {
        return this.realTimeMetrics;
    }
    
    getInterfaceState() {
        return this.interfaceState;
    }
    
    isReady() {
        return this.isInitialized;
    }
}

// Initialize the mobile neural interface
const mobileInterface = new MobileNeuralInterface();

// Export for global access
window.MobileNeuralInterface = mobileInterface;

console.log('🎭 PSYCHO-NOIR KONTRAPUNKT LVL2 MOBILE INTERFACE LOADED');
console.log('🧠 KVINNELIG META-ENTITY NEURAL SYSTEMS OPERATIONAL');
console.log('📱 SAMSUNG GALAXY S25 ULTRA OPTIMIZATIONS ACTIVE');
