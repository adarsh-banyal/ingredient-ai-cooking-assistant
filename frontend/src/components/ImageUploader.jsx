import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { UploadCloud, Camera, ArrowRight } from 'lucide-react';
import './ImageUploader.css';

const ImageUploader = ({ onImageSelect, previewUrls, onProcess, hasFile }) => {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const selectedFiles = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
            if (selectedFiles.length > 0) {
                onImageSelect(selectedFiles);
            }
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            onImageSelect(Array.from(e.target.files));
        }
    };

    return (
        <div className="glass-card uploader-card">
            {!hasFile ? (
                <motion.div
                    className={`dropzone ${isDragging ? 'active' : ''}`}
                    onClick={handleClick}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept="image/*"
                        multiple
                        className="hidden-input"
                    />
                    <motion.div
                        animate={{ y: [0, -10, 0] }}
                        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
                    >
                        <UploadCloud size={64} className="upload-icon" />
                    </motion.div>
                    <div className="upload-text">Click to upload or drag & drop</div>
                    <div className="upload-subtext">Support multiple images (Max 5MB each)</div>
                </motion.div>
            ) : (
                <div className="preview-container" onClick={handleClick}>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept="image/*"
                        multiple
                        className="hidden-input"
                    />
                    <div className="preview-image-wrapper">
                        <img src={previewUrls[0]} alt="Ingredients Preview" className="preview-image" />
                        {previewUrls.length > 1 && (
                            <div className="image-count-badge">+{previewUrls.length - 1} more</div>
                        )}
                    </div>
                    <div className="preview-overlay">
                        <button className="change-btn">
                            <Camera size={18} style={{ marginRight: '8px', display: 'inline' }} />
                            Add/Change Photos ({previewUrls.length})
                        </button>
                    </div>
                </div>
            )}

            {hasFile && (
                <motion.div
                    className="action-container"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <motion.button
                        className="primary-btn"
                        onClick={onProcess}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        Find Recipes
                        <ArrowRight size={20} />
                    </motion.button>
                </motion.div>
            )}
        </div>
    );
};

export default ImageUploader;
