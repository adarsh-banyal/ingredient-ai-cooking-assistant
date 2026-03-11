import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, ChefHat } from 'lucide-react';
import ImageUploader from './components/ImageUploader';
import RecipeResults from './components/RecipeResults';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [activeIngredients, setActiveIngredients] = useState([]);
  const [activeFilters, setActiveFilters] = useState([]);
  const [error, setError] = useState(null);

  const handleImageSelect = (selectedFile) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResults(null);
    setError(null);
  };

  const handleProcessImage = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/detect-recipes', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process image. Make sure the backend is running.');
      }

      const data = await response.json();
      setResults(data);
      // Initialize active ingredients from detection (handling both old string and new object formats)
      const initialIngredients = (data.detected_ingredients || []).map(item =>
        typeof item === 'string' ? item : item.label
      );
      setActiveIngredients(initialIngredients);
    } catch (err) {
      console.error(err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchRecipesByIngredients = async (ingredients, filters = activeFilters) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/search-recipes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredients,
          filters: filters.length > 0 ? filters : null
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to search recipes.');
      }

      const data = await response.json();
      // Keep the existing detected_ingredients in results, just update recipes
      setResults(prev => ({
        ...prev,
        recipes: data.recipes
      }));
    } catch (err) {
      console.error(err);
      setError(err.message || 'An unexpected error occurred during search.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddIngredient = (ingredient) => {
    const newIngredients = [...activeIngredients, ingredient.toLowerCase().trim()];
    setActiveIngredients(newIngredients);
    fetchRecipesByIngredients(newIngredients, activeFilters);
  };

  const handleRemoveIngredient = (ingredient) => {
    const newIngredients = activeIngredients.filter(i => i !== ingredient);
    setActiveIngredients(newIngredients);
    fetchRecipesByIngredients(newIngredients, activeFilters);
  };

  const handleFilterToggle = (filter) => {
    const newFilters = activeFilters.includes(filter)
      ? activeFilters.filter(f => f !== filter)
      : [...activeFilters, filter];

    setActiveFilters(newFilters);
    fetchRecipesByIngredients(activeIngredients, newFilters);
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setResults(null);
    setActiveIngredients([]);
    setActiveFilters([]);
    setError(null);
  };

  return (
    <>
      <div className="bg-gradient-mesh"></div>

      <div className="app-container">
        <header className="header">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex-center"
            style={{ marginBottom: '1rem' }}
          >
            <div style={{
              background: 'var(--color-accent-gradient)',
              padding: '1rem',
              borderRadius: 'var(--radius-lg)',
              boxShadow: 'var(--shadow-glow)'
            }}>
              <ChefHat size={32} color="white" />
            </div>
          </motion.div>

          <motion.h1
            className="title text-gradient"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            Recipe AI
          </motion.h1>

          <motion.p
            className="subtitle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Snap a photo of your ingredients and let AI craft the perfect recipe for you.
          </motion.p>
        </header>

        <main className="main-content">
          <AnimatePresence mode="wait">
            {!results && !isLoading && (
              <motion.div
                key="uploader"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20, transition: { duration: 0.2 } }}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                <ImageUploader
                  onImageSelect={handleImageSelect}
                  previewUrl={previewUrl}
                  onProcess={handleProcessImage}
                  hasFile={!!file}
                />
              </motion.div>
            )}

            {isLoading && (
              <motion.div
                key="loading"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                className="glass-card loading-container"
                style={{ borderRadius: 'var(--radius-lg)' }}
              >
                <div className="spinner animate-spin"></div>
                <div className="loading-text">Analyzing ingredients & finding recipes...</div>
              </motion.div>
            )}

            {error && (
              <motion.div
                key="error"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, transition: { duration: 0.2 } }}
                className="error-container"
              >
                <AlertCircle size={24} />
                <p>{error}</p>
              </motion.div>
            )}

            {results && !isLoading && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <RecipeResults
                  data={results}
                  activeIngredients={activeIngredients}
                  onAddIngredient={handleAddIngredient}
                  onRemoveIngredient={handleRemoveIngredient}
                  activeFilters={activeFilters}
                  onFilterToggle={handleFilterToggle}
                  onReset={handleReset}
                  previewUrl={previewUrl}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </>
  );
}

export default App;
