import { useState } from 'react';

const usePrescription = (setStep, setLoading) => {
  const [prescriptionImage, setPrescriptionImage] = useState('https://via.placeholder.com/400x600.png?text=Sample+Prescription');
  const [loading, setLoadingState] = useState(false);

  const handleImageUpload = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const imageUrl = URL.createObjectURL(file);
      setPrescriptionImage(imageUrl);
      setStep('processing');
      setLoadingState(true);
      
      setTimeout(() => {
        setLoadingState(false);
        setStep('schedule');
      }, 2000);
    }
  };

  const handleCameraCapture = () => {
    document.getElementById('fileInput').click();
  };

  const handleReset = () => {
    setPrescriptionImage(null);
    setStep('upload');
  };

  const handleBackToSchedule = () => {
    setStep('schedule');
  };

  return {
    prescriptionImage,
    loading,
    handleImageUpload,
    handleCameraCapture,
    handleReset,
    handleBackToSchedule,
    setPrescriptionImage,
    setLoading: setLoadingState
  };
};

export default usePrescription;