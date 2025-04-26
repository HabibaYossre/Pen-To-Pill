import React from 'react';
import { ArrowLeft } from 'lucide-react';

const ProcessingStep = ({ prescriptionImage, loading, onBack }) => {
  return (
    <div className="text-center p-8 border rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <button 
          onClick={onBack}
          className="flex items-center text-gray-600 hover:text-blue-600"
        >
          <ArrowLeft size={18} className="mr-1" />
          Back to Upload
        </button>
        <h2 className="text-xl font-semibold">Processing Prescription</h2>
        <div className="w-8"></div>
      </div>
      
      <div className="mb-4">
        {prescriptionImage && (
          <img
            src={prescriptionImage}
            alt="Prescription"
            className="max-h-64 mx-auto rounded-lg shadow"
          />
        )}
      </div>
      
      <p className="text-gray-600 mt-2 mb-6">
        Analyzing image and extracting medication information...
      </p>
      
      <div className="flex justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    </div>
  );
};

export default ProcessingStep;