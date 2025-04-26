import React from 'react';
import { X, ImageIcon } from 'lucide-react';
import CardsView from './CardsView';
import CalendarView from './CalendarView';
import FilterControls from './FilterControls';

const ScheduleStep = ({
  prescriptionImage,
  medicines,
  filteredMedicines,
  filter,
  searchTerm,
  viewMode,
  onReset,
  onSetFilter,
  onSetSearchTerm,
  onSetViewMode,
  onShowImageUpload,
  onRemoveImage
}) => {
  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Your Medication Schedule</h2>
        <button
          onClick={onReset}
          className="flex items-center text-gray-600 hover:text-red-600"
        >
          <X size={18} className="mr-1" />
          New Prescription
        </button>
      </div>
      
      <div className="mb-6">
        <details className="bg-gray-50 rounded-lg p-2">
          <summary className="cursor-pointer p-2">View Prescription Image</summary>
          <div className="p-2">
            <img
              src={prescriptionImage}
              alt="Prescription"
              className="max-h-64 mx-auto rounded-lg shadow"
            />
          </div>
        </details>
      </div>
      
      <FilterControls
        filter={filter}
        searchTerm={searchTerm}
        viewMode={viewMode}
        onSetFilter={onSetFilter}
        onSetSearchTerm={onSetSearchTerm}
        onSetViewMode={onSetViewMode}
      />
      
      {viewMode === 'cards' ? (
        <CardsView
          medicines={filteredMedicines}
          onShowImageUpload={onShowImageUpload}
          onRemoveImage={onRemoveImage}
        />
      ) : (
        <CalendarView
          medicines={filteredMedicines}
          onShowImageUpload={onShowImageUpload}
          onRemoveImage={onRemoveImage}
        />
      )}
      
      {filteredMedicines.length === 0 && (
        <div className="text-center p-8 text-gray-500">
          No medicines found matching your criteria
        </div>
      )}
    </div>
  );
};

export default ScheduleStep;