import React from 'react';
import { Upload, Camera, X } from 'lucide-react';

const ImageUploadModal = ({ onClose, onUpload, onCameraCapture }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg max-w-md w-full">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Upload Medication Image</h3>
          <button onClick={onClose}>
            <X size={20} />
          </button>
        </div>
        <p className="mb-4 text-gray-600">Upload an image of the medication for visual reference</p>
        <input
          type="file"
          id="medImageInput"
          accept="image/*"
          className="hidden"
          onChange={onUpload}
        />
        <div className="flex gap-4">
          <button
            onClick={() => document.getElementById('medImageInput').click()}
            className="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            <Upload size={16} />
            Upload
          </button>
          <button
            onClick={onCameraCapture}
            className="flex-1 flex items-center justify-center gap-2 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            <Camera size={16} />
            Camera
          </button>
        </div>
        <div className="mt-4 flex justify-center">
          <button
            onClick={onClose}
            className="text-gray-600 hover:text-gray-800 px-4 py-2"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageUploadModal;