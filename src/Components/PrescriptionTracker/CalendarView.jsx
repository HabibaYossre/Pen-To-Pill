import React from 'react';
import { ImageIcon, X } from 'lucide-react';
import { determineCategory } from './utils/medicineUtils';

const CalendarView = ({ medicines, onShowImageUpload, onRemoveImage }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="col-span-1">
        <h2 className="font-bold mb-2 text-center bg-yellow-200 py-2 rounded-t-lg">Morning</h2>
        <div className="border rounded-b-lg p-4 space-y-3">
          {medicines
            .filter(med => determineCategory(med.frequency) === "morning")
            .map((med, index) => (
              <div key={index} className="p-2 bg-yellow-50 rounded border border-yellow-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{med.name}</p>
                    <p className="text-sm text-gray-600">{med.frequency}</p>
                  </div>
                  {med.image ? (
                    <div className="relative">
                      <img 
                        src={med.image} 
                        alt="Medication" 
                        className="w-12 h-12 object-cover rounded-md"
                      />
                      <button 
                        onClick={() => onRemoveImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => onShowImageUpload(medicines.indexOf(med))}
                      className="p-1 bg-blue-100 hover:bg-blue-200 rounded-full"
                    >
                      <ImageIcon size={16} />
                    </button>
                  )}
                </div>
              </div>
            ))}
        </div>
      </div>
      
      <div className="col-span-1">
        <h2 className="font-bold mb-2 text-center bg-orange-200 py-2 rounded-t-lg">Afternoon</h2>
        <div className="border rounded-b-lg p-4 space-y-3">
          {medicines
            .filter(med => determineCategory(med.frequency) === "afternoon")
            .map((med, index) => (
              <div key={index} className="p-2 bg-orange-50 rounded border border-orange-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{med.name}</p>
                    <p className="text-sm text-gray-600">{med.frequency}</p>
                  </div>
                  {med.image ? (
                    <div className="relative">
                      <img 
                        src={med.image} 
                        alt="Medication" 
                        className="w-12 h-12 object-cover rounded-md"
                      />
                      <button 
                        onClick={() => onRemoveImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => onShowImageUpload(medicines.indexOf(med))}
                      className="p-1 bg-blue-100 hover:bg-blue-200 rounded-full"
                    >
                      <ImageIcon size={16} />
                    </button>
                  )}
                </div>
              </div>
            ))}
        </div>
      </div>
      
      <div className="col-span-1">
        <h2 className="font-bold mb-2 text-center bg-indigo-200 py-2 rounded-t-lg">Evening</h2>
        <div className="border rounded-b-lg p-4 space-y-3">
          {medicines
            .filter(med => determineCategory(med.frequency) === "evening")
            .map((med, index) => (
              <div key={index} className="p-2 bg-indigo-50 rounded border border-indigo-300">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{med.name}</p>
                    <p className="text-sm text-gray-600">{med.frequency}</p>
                  </div>
                  {med.image ? (
                    <div className="relative">
                      <img 
                        src={med.image} 
                        alt="Medication" 
                        className="w-12 h-12 object-cover rounded-md"
                      />
                      <button 
                        onClick={() => onRemoveImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => onShowImageUpload(medicines.indexOf(med))}
                      className="p-1 bg-blue-100 hover:bg-blue-200 rounded-full"
                    >
                      <ImageIcon size={16} />
                    </button>
                  )}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default CalendarView;