import React from 'react';
import { Upload, Camera, ArrowLeft } from 'lucide-react';

const UploadStep = ({ onBack, onUpload, onCameraCapture }) => {
  return (
    <div className="text-center p-8 border-2 border-dashed border-gray-300 rounded-lg">
      <input
        type="file"
        id="fileInput"
        accept="image/*"
        className="hidden"
        onChange={onUpload}
      />
      
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <button 
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-blue-600"
          >
            <ArrowLeft size={18} className="mr-1" />
            Back to Schedule
          </button>
          <h2 className="text-xl font-semibold">Upload Prescription Image</h2>
          <div className="w-8"></div>
        </div>
        <p className="text-gray-600 mb-6">
          Take a photo of your prescription or upload an existing image to extract medication information
        </p>
        
        <div className="flex flex-col md:flex-row justify-center gap-4">
          <button
            onClick={() => document.getElementById('fileInput').click()}
            className="flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
          >
            <Upload size={20} />
            Upload Image
          </button>
          
          <button
            onClick={onCameraCapture}
            className="flex items-center justify-center gap-2 bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
          >
            <Camera size={20} />
            Take Photo
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadStep;