import React, { useState } from 'react';
import axios from 'axios';
import './Upload.css';

function Upload() {
    const [file, setFile] = useState(null);
    const [imageUrl, setImageUrl] = useState('');
    const [originalText, setOriginalText] = useState('');
    const [correctedText, setCorrectedText] = useState('');
    const [translation, setTranslation] = useState('');

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setFile(file);
            const reader = new FileReader();
            reader.onload = function(e) {
                setImageUrl(e.target.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleTranslate = async () => {
        if (!correctedText) return; 
        try {
            const response = await axios.post('http://localhost:8000/api/translate/', {
                text: correctedText.replace('Corrected Text: ', ''),
            });
            setTranslation(`Translated Text: ${response.data.translated}`);
        } catch (error) {
            console.error('An error occurred during translation:', error);
        }
    };

    const handleSpeech = async () => {
        if (!translation) return; 
        try {
            await axios.post('http://localhost:8000/api/speech/', {
                text: translation.replace('Translated Text: ', ''),
                language: 0, // Assuming 0 is for Polish
            });
        } catch (error) {
            console.error('An error occurred during speech synthesis:', error);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setOriginalText("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setOriginalText(`Original Text: ${response.data.original}`);
            setCorrectedText(`Corrected Text: ${response.data.corrected}`);
            setTranslation(''); 
        } catch (error) {
            setOriginalText('An error occurred while uploading the file.');
            setCorrectedText('');
            setTranslation('');
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload your file</h2>
            <form onSubmit={handleSubmit} className="upload-form">
                <input type="file" onChange={handleFileChange} accept="image/*" className="file-input" />
                <button type="submit" className="button">Upload File</button>
                <button onClick={handleTranslate} disabled={!correctedText} className="button">Translate</button>
                <button onClick={handleSpeech} disabled={!translation} className="button">Read Aloud</button>
            </form>
            <div className="image-display">
                {imageUrl && <img src={imageUrl} alt="Uploaded" style={{ maxWidth: '100%', maxHeight: '400px' }} />}
            </div>
            <div className="output">
                {originalText && <p>{originalText}</p>}
                {correctedText && <p>{correctedText}</p>}
                {translation && <p>{translation}</p>}
            </div>
        </div>
    );
}

export default Upload;
