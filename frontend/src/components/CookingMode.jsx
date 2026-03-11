import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronLeft, ChevronRight, CheckCircle, List } from 'lucide-react';
import './RecipeResults.css';

const CookingMode = ({ recipe, onClose }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const { name, steps = [], ingredients = [] } = recipe;

    const progress = ((currentStep + 1) / steps.length) * 100;

    const nextStep = () => {
        if (currentStep < steps.length - 1) {
            setCurrentStep(currentStep + 1);
        }
    };

    const prevStep = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    return (
        <motion.div
            className="cooking-mode-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
        >
            <div className="cooking-mode-container glass-card">
                <header className="cooking-header">
                    <div className="cooking-title-group">
                        <h2 className="cooking-recipe-name">{name}</h2>
                        <div className="cooking-progress-text">Step {currentStep + 1} of {steps.length}</div>
                    </div>
                    <button className="close-cooking-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </header>

                <div className="progress-bar-container">
                    <motion.div
                        className="progress-bar-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.3 }}
                    />
                </div>

                <div className="cooking-content">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={currentStep}
                            className="step-content"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ duration: 0.3 }}
                        >
                            <p className="step-instruction">{steps[currentStep]}</p>
                        </motion.div>
                    </AnimatePresence>
                </div>

                <footer className="cooking-footer">
                    <button
                        className="cooking-nav-btn secondary-btn"
                        onClick={prevStep}
                        disabled={currentStep === 0}
                    >
                        <ChevronLeft size={20} />
                        Back
                    </button>

                    {currentStep < steps.length - 1 ? (
                        <button className="cooking-nav-btn add-ing-btn" onClick={nextStep}>
                            Next
                            <ChevronRight size={20} />
                        </button>
                    ) : (
                        <button className="cooking-nav-btn finish-btn" onClick={onClose}>
                            <CheckCircle size={20} />
                            Finish
                        </button>
                    )}
                </footer>
            </div>
        </motion.div>
    );
};

export default CookingMode;
