import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, RefreshCw, ChefHat, Target, ChevronDown, ChevronUp, BookOpen, List, AlertCircle } from 'lucide-react';
import './RecipeResults.css';

const RecipeCard = ({ recipe, itemVariants }) => {
    const { name, score, ingredients = [], steps = [], missing_ingredients = [] } = recipe;
    const [isExpanded, setIsExpanded] = useState(false);

    const getScoreColor = (scoreValue) => {
        if (scoreValue >= 4) return 'score-low';
        if (scoreValue >= 2) return 'score-med';
        return 'score-high';
    };

    return (
        <motion.div variants={itemVariants} className="glass-card recipe-card">
            <div className="recipe-card-header">
                <h4 className="recipe-name">{name}</h4>
                <div className="recipe-meta">
                    <div className={`match-score ${getScoreColor(score)}`}>
                        <Target size={16} />
                        <span>Score: {score.toFixed(2)}</span>
                    </div>
                </div>
            </div>

            {missing_ingredients.length > 0 && (
                <div className="missing-alert-inline">
                    <AlertCircle size={14} />
                    <span>Missing {missing_ingredients.length} item{missing_ingredients.length > 1 ? 's' : ''}</span>
                </div>
            )}

            <div className="recipe-actions">
                <button
                    className="expand-btn"
                    onClick={() => setIsExpanded(!isExpanded)}
                >
                    {isExpanded ? "Hide Recipe" : "View Recipe"}
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                </button>
            </div>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        className="recipe-details"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                    >
                        {missing_ingredients.length > 0 && (
                            <div className="detail-section missing-section">
                                <h5 className="detail-title missing-text">
                                    <AlertCircle size={16} />
                                    Missing Ingredients
                                </h5>
                                <ul className="detail-list missing-list">
                                    {missing_ingredients.map((ing, i) => (
                                        <li key={i}>{ing}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        <div className="detail-section">
                            <h5 className="detail-title">
                                <List size={16} />
                                Required Ingredients
                            </h5>
                            <ul className="detail-list ingredients">
                                {ingredients.map((ing, i) => (
                                    <li key={i}>{ing}</li>
                                ))}
                            </ul>
                        </div>

                        <div className="detail-section">
                            <h5 className="detail-title">
                                <BookOpen size={16} />
                                Instructions
                            </h5>
                            <ol className="detail-list steps">
                                {steps.map((step, i) => (
                                    <li key={i}>{step}</li>
                                ))}
                            </ol>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};

const RecipeResults = ({ data, activeIngredients, onAddIngredient, onRemoveIngredient, activeFilters, onFilterToggle, onReset, previewUrl }) => {
    const { recipes = [] } = data;
    const [newIngredient, setNewIngredient] = useState("");

    const handleAdd = (e) => {
        e.preventDefault();
        if (newIngredient.trim()) {
            onAddIngredient(newIngredient);
            setNewIngredient("");
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
    };

    return (
        <div className="results-container">
            <motion.div
                className="glass-card"
                style={{ padding: '1.5rem', borderRadius: 'var(--radius-lg)' }}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="results-header">
                    {previewUrl && (
                        <div className="results-image-wrapper">
                            <img src={previewUrl} alt="Analyzed" className="results-image" />
                        </div>
                    )}

                    <div className="ingredients-section">
                        <h3 className="section-title">
                            <Sparkles size={20} color="var(--color-accent-secondary)" />
                            Detected Ingredients
                        </h3>

                        {activeIngredients.length > 0 ? (
                            <div className="ingredients-list">
                                <AnimatePresence>
                                    {activeIngredients.map((ing, idx) => (
                                        <motion.span
                                            key={ing}
                                            className="ingredient-pill editable"
                                            initial={{ opacity: 0, scale: 0.8 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            exit={{ opacity: 0, scale: 0.8 }}
                                            transition={{ delay: idx * 0.05 }}
                                        >
                                            {ing}
                                            <button
                                                className="remove-ing-btn"
                                                onClick={() => onRemoveIngredient(ing)}
                                                aria-label={`Remove ${ing}`}
                                            >
                                                ×
                                            </button>
                                        </motion.span>
                                    ))}
                                </AnimatePresence>
                            </div>
                        ) : (
                            <p style={{ color: 'var(--color-text-muted)', marginBottom: '1rem' }}>
                                No ingredients detected or added.
                            </p>
                        )}

                        <form onSubmit={handleAdd} className="add-ingredient-form">
                            <input
                                type="text"
                                value={newIngredient}
                                onChange={(e) => setNewIngredient(e.target.value)}
                                placeholder="Add an ingredient..."
                                className="ingredient-input"
                            />
                            <button type="submit" className="add-ing-btn">Add</button>
                        </form>
                    </div>

                    <div className="filters-section">
                        <h3 className="section-title">
                            <ChefHat size={20} color="var(--color-accent-primary)" />
                            Dietary Filters
                        </h3>
                        <div className="filters-list">
                            {['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free'].map(filter => (
                                <label key={filter} className={`filter-chip ${activeFilters.includes(filter) ? 'active' : ''}`}>
                                    <input
                                        type="checkbox"
                                        checked={activeFilters.includes(filter)}
                                        onChange={() => onFilterToggle(filter)}
                                        className="hidden-checkbox"
                                    />
                                    {filter}
                                </label>
                            ))}
                        </div>
                    </div>
                </div>
            </motion.div>

            <div className="recipes-section">
                <h3 className="section-title" style={{ marginBottom: '1.5rem', marginLeft: '0.5rem' }}>
                    <ChefHat size={22} color="var(--color-accent-primary)" />
                    Suggested Recipes
                </h3>

                {recipes.length > 0 ? (
                    <motion.div
                        className="recipes-grid"
                        variants={containerVariants}
                        initial="hidden"
                        animate="visible"
                    >
                        {recipes.map((recipe, idx) => (
                            <RecipeCard key={idx} recipe={recipe} itemVariants={itemVariants} />
                        ))}
                    </motion.div>
                ) : (
                    <div className="glass-card empty-state">
                        <p>No suitable recipes found based on these ingredients.</p>
                    </div>
                )}
            </div>

            <div className="reset-container">
                <motion.button
                    className="secondary-btn"
                    onClick={onReset}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <RefreshCw size={18} />
                    Start Over
                </motion.button>
            </div>
        </div>
    );
};

export default RecipeResults;
