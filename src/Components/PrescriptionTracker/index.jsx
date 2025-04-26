// import React, { useState } from 'react';
// import UploadStep from './UploadStep';
// import ProcessingStep from './ProcessingStep';
// import ScheduleStep from './ScheduleStep';
// import ImageUploadModal from './ImageUploadModal';
// import usePrescription from './hooks/usePrescription';
// import useMedicine from './hooks/useMedicine';
// import './styles.css';

// const PrescriptionTracker = () => {
//   const [step, setStep] = useState('schedule');
//   const [viewMode, setViewMode] = useState('cards');
//   const [showImageUpload, setShowImageUpload] = useState(false);
//   const [selectedMed, setSelectedMed] = useState(null);

//   const {
//     prescriptionImage,
//     loading,
//     handleImageUpload,
//     handleCameraCapture,
//     handleReset,
//     handleBackToSchedule,
//     setPrescriptionImage,
//     setLoading
//   } = usePrescription(setStep);

//   const {
//     medicines,
//     filter,
//     searchTerm,
//     filteredMedicines,
//     setFilter,
//     setSearchTerm,
//     setMedicines,
//     removeImage
//   } = useMedicine();

//   return (
//     <div className='h-screen w-screen bg-hero-pattern bg-cover bg-center bg-no-repeat'>
//       <div className="absolute inset-0 bg-black opacity-80 z-10 bg-no-repeat">
//         <div className="max-w-4xl mx-auto p-4 font-sans">
//           {step === 'upload' && (
//             <UploadStep 
//               onBack={handleBackToSchedule}
//               onUpload={handleImageUpload}
//               onCameraCapture={handleCameraCapture}
//             />
//           )}

//           {step === 'processing' && (
//             <ProcessingStep 
//               prescriptionImage={prescriptionImage}
//               loading={loading}
//               onBack={() => {
//                 setStep('upload');
//                 setPrescriptionImage(null);
//               }}
//             />
//           )}

//           {step === 'schedule' && (
//             <ScheduleStep
//               prescriptionImage={prescriptionImage}
//               medicines={medicines}
//               filteredMedicines={filteredMedicines}
//               filter={filter}
//               searchTerm={searchTerm}
//               viewMode={viewMode}
//               onReset={handleReset}
//               onSetFilter={setFilter}
//               onSetSearchTerm={setSearchTerm}
//               onSetViewMode={setViewMode}
//               onShowImageUpload={(index) => {
//                 setSelectedMed(index);
//                 setShowImageUpload(true);
//               }}
//               onRemoveImage={removeImage}
//             />
//           )}

//           {showImageUpload && (
//             <ImageUploadModal
//               onClose={() => setShowImageUpload(false)}
//               onUpload={handleImageUpload}
//               onCameraCapture={handleCameraCapture}
//             />
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default PrescriptionTracker;

import React, { useState } from 'react';
import { Camera, Upload, X, ArrowLeft } from 'lucide-react';
import UploadStep from './UploadStep';
import ProcessingStep from './ProcessingStep';
import ScheduleStep from './ScheduleStep';
import ImageUploadModal from './ImageUploadModal';
import usePrescription from './hooks/usePrescription';
import useMedicine from './hooks/useMedicine';
import './styles.css';
import Background from '../../Assets/background.png';

const PrescriptionTracker = () => {
  const [step, setStep] = useState('schedule');
  const [viewMode, setViewMode] = useState('cards');
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [selectedMed, setSelectedMed] = useState(null);

  const {
    prescriptionImage,
    loading,
    handleImageUpload,
    handleCameraCapture,
    handleReset,
    handleBackToSchedule,
    setPrescriptionImage,
    setLoading
  } = usePrescription(setStep);

  const {
    medicines,
    filter,
    searchTerm,
    filteredMedicines,
    setFilter,
    setSearchTerm,
    setMedicines,
    removeImage
  } = useMedicine();

  return (
    <div className="relative min-h-screen">
      {/* Fixed background with overlay */}
      <div className="fixed inset-0 -z-10">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${Background})` }}
        />
        <div className="absolute inset-0 bg-black opacity-80" />
      </div>
      
      {/* Content area with proper navbar spacing */}
      <div className="relative z-10 pt-24 min-h-screen">
        <div className="max-w-4xl mx-100 p-4 font-sans">
          {step === 'upload' && (
            <UploadStep 
              onBack={handleBackToSchedule}
              onUpload={handleImageUpload}
              onCameraCapture={handleCameraCapture}
            />
          )}

          {step === 'processing' && (
            <ProcessingStep 
              prescriptionImage={prescriptionImage}
              loading={loading}
              onBack={() => {
                setStep('upload');
                setPrescriptionImage(null);
              }}
            />
          )}

          {step === 'schedule' && (
            <ScheduleStep
              prescriptionImage={prescriptionImage}
              medicines={medicines}
              filteredMedicines={filteredMedicines}
              filter={filter}
              searchTerm={searchTerm}
              viewMode={viewMode}
              onReset={handleReset}
              onSetFilter={setFilter}
              onSetSearchTerm={setSearchTerm}
              onSetViewMode={setViewMode}
              onShowImageUpload={(index) => {
                setSelectedMed(index);
                setShowImageUpload(true);
              }}
              onRemoveImage={removeImage}
            />
          )}

          {showImageUpload && (
            <ImageUploadModal
              onClose={() => setShowImageUpload(false)}
              onUpload={handleImageUpload}
              onCameraCapture={handleCameraCapture}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default PrescriptionTracker;