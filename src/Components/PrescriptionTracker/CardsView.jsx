import React from 'react';
import { Clock, ImageIcon, X} from 'lucide-react';
import { getTimeIcon, getBackgroundColor } from './utils/medicineUtils';

const CardsView = ({ medicines, onShowImageUpload, onRemoveImage }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {medicines.map((medicine, index) => (
        <div key={index} className={`p-4 rounded-lg shadow ${getBackgroundColor(medicine.frequency)}`}>
          <div className="flex items-center mb-2">
            <span className="text-2xl mr-2">{getTimeIcon(medicine.frequency)}</span>
            <h2 className="text-lg font-semibold truncate">{medicine.name}</h2>
          </div>
          <div className="text-gray-700 font-medium flex items-center">
            <Clock size={16} className="mr-1" />
            {medicine.frequency}
          </div>
          {medicine.image && (
            <div className="mt-2 relative">
              <img 
                src={medicine.image} 
                alt="Medication" 
                className="w-full h-24 object-cover rounded-md"
              />
              <button 
                onClick={() => onRemoveImage(index)}
                className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 w-5 h-5 flex items-center justify-center"
              >
                <X size={12} />
              </button>
            </div>
          )}
          {!medicine.image && (
            <button 
              onClick={() => onShowImageUpload(index)}
              className="mt-2 flex items-center text-sm text-blue-600 hover:text-blue-800"
            >
              <ImageIcon size={14} className="mr-1" />
              Add medication image
            </button>
          )}
        </div>
      ))}
    </div>
  );
};

export default CardsView;