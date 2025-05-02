import { useState, useRef } from 'react';
import { Upload, Camera, X, Loader2, Check, AlertCircle } from 'lucide-react';
import { addPrescription } from '../../dbOperations';
import axios from 'axios';

  const AddPrescription = ({setMedicines}) => {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [isTextExtracted, setIsTextExtracted] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [prescriptions, setPrescriptions] = useState([]);

  
  const fileInputRef = useRef(null);

  
  
  const handleFileChange = (e) => {
    setError('');
    setSuccess(false);
    setExtractedText('');
    
    const file = e.target.files[0];
    if (!file) return;
    
    // Validate file type
    if (!file.type.includes('image/')) {
      setError('Please upload an image file');
      return;
    }
    
    setImage(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };
  
  const handleCameraClick = () => {
    fileInputRef.current.click();
  };
  
  const handleRemoveImage = () => {
    setImage(null);
    setPreviewUrl(null);
    setExtractedText('');
    setError('');
    setSuccess(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  const extractText = async () => {
    if (!image) {
      setError('Please upload a prescription image first');
      return;
    }
  
    try {
      setIsProcessing(true);
      setError('');
      setSuccess(false);
  
      const formData = new FormData();
      formData.append('file', image);
  
      const response = await axios.post("http://localhost:8000/process_prescription/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      const data = response.data.prescriptions;
  
      if (!Array.isArray(data) || data.length === 0) {
        setError('No text could be extracted. Please try again with a clearer image.');
        setExtractedText('');
        setIsProcessing(false);
        return;
      }
      if (!Array.isArray(data)) {
        console.error('Unexpected response format:', data);
        setError('Server returned unexpected data.');
        return;
      }

  
      console.log("data", data);
  
      const text = data
        .map(item => `${item.medicine}: ${item.dosage}`)
        .join('\n');
      console.log("extractedWords", text);
  
      await addPrescription(data);
      setMedicines(prev => [...prev, ...data]);
      setExtractedText(text.trim());
      setSuccess(true);
    } catch (err) {
      setError('Failed to extract text from image. Please try again.');
      console.error('OCR Error:', err);
    } finally {
      setIsProcessing(false);
    }
  };
  
  
  

  
  return (
    <div className="min-h-screen w-full flex items-center justify-center">
    <div className="w-full max-w-4xl p-6">
    <h1 className="text-3xl font-bold mb-6 text-center">Add Prescription</h1>
  
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-center mb-4">
            <h2 className="text-xl font-semibold">Upload Prescription Image</h2>
          </div>
  
          <div className="mb-6">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
              capture="environment"
            />
  
            {!previewUrl ? (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
                <div className="flex flex-col items-center justify-center gap-4">
                  <button
                    onClick={() => fileInputRef.current.click()}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md flex items-center gap-2"
                  >
                    <Upload size={20} />
                    Upload Image
                  </button>
  
                  <button
                    onClick={handleCameraClick}
                    className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md flex items-center gap-2"
                  >
                    <Camera size={20} />
                    Take Photo
                  </button>
  
                  <p className="text-gray-500 text-sm mt-2">
                    Please upload a clear image of your prescription
                  </p>
                </div>
              </div>
            ) : (
              <div className="relative">
                <img
                  src={previewUrl}
                  alt="Prescription preview"
                  className="w-full h-64 object-contain border rounded-lg"
                />
                <button
                  onClick={handleRemoveImage}
                  className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-1 rounded-full"
                >
                  <X size={20} />
                </button>
              </div>
            )}
          </div>
  
          {previewUrl && (
            <div className="flex justify-center mb-6">
              <button
                onClick={extractText}
                disabled={isProcessing}
                className={`px-6 py-2 rounded-md flex items-center gap-2 ${
                  isProcessing
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                {isProcessing ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>Extract Text</>
                )}
              </button>
            </div>
          )}
  
          {error && (
            <div className="mb-4 p-4 bg-red-100 border-l-4 border-red-500 text-red-700 flex items-center gap-2">
              <AlertCircle size={20} />
              {error}
            </div>
          )}
  
          {success && (
            <div className="mb-4 p-4 bg-green-100 border-l-4 border-green-500 text-green-700 flex items-center gap-2">
              <Check size={20} />
              Text extracted successfully!
            </div>
          )}
        </div>
      </div>
    </div>
  );
  
}
export default AddPrescription;

