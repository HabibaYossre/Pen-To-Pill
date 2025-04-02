import React, { useState } from 'react';
import { Camera, Upload, Calendar, Clock, Search, X, Image as ImageIcon, ArrowLeft } from 'lucide-react';

const PrescriptionTracker = () => {
  // Start directly with the schedule view and sample data
  const [step, setStep] = useState('schedule');
  const [prescriptionImage, setPrescriptionImage] = useState('https://via.placeholder.com/400x600.png?text=Sample+Prescription');
  const [medicines, setMedicines] = useState([
    { name: "Doxycycline / دوكسيسيكلين", frequency: "كل ١٢ ساعة", image: null },
    { name: "Diclofenac / ديكلوفيناك", frequency: "كل ٦ ساعات", image: null },
    { name: "Metronidazole / ميترونيدازول", frequency: "قبل النوم", image: null },
    { name: "Azithromycin / أزيثروميسين", frequency: "كل ٨ ساعات", image: null },
    { name: "Paracetamol / باراسيتامول", frequency: "عند اللزوم", image: null },
    { name: "Amoxicillin / أموكسيسيلين", frequency: "قبل الفطار", image: null },
    { name: "Ibuprofen / إيبوبروفين", frequency: "بعد الغداء", image: null },
    { name: "Mupirocin / موبيروسين", frequency: "مرتين يومياً", image: null },
    { name: "Omeprazole / أوميبرازول", frequency: "قبل العشاء", image: null },
    { name: "Cetirizine / سيتريزين", frequency: "في الصباح", image: null }
  ]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('cards');
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [selectedMed, setSelectedMed] = useState(null);

  // Function to handle image upload
  const handleImageUpload = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const imageUrl = URL.createObjectURL(file);
      
      if (showImageUpload && selectedMed !== null) {
        // Update medicine image
        const updatedMedicines = [...medicines];
        updatedMedicines[selectedMed].image = imageUrl;
        setMedicines(updatedMedicines);
        setShowImageUpload(false);
        setSelectedMed(null);
      } else {
        // Prescription image upload
        setPrescriptionImage(imageUrl);
        setStep('processing');
        setLoading(true);
        
        // Simulate processing the image
        setTimeout(() => {
          const extractedMedicines = [
            { name: "Doxycycline / دوكسيسيكلين", frequency: "كل ١٢ ساعة", image: null },
            { name: "Diclofenac / ديكلوفيناك", frequency: "كل ٦ ساعات", image: null },
            { name: "Metronidazole / ميترونيدازول", frequency: "قبل النوم", image: null },
            { name: "Azithromycin / أزيثروميسين", frequency: "كل ٨ ساعات", image: null },
            { name: "Paracetamol / باراسيتامول", frequency: "عند اللزوم", image: null },
            { name: "Amoxicillin / أموكسيسيلين", frequency: "قبل الفطار", image: null },
            { name: "Ibuprofen / إيبوبروفين", frequency: "بعد الغداء", image: null },
            { name: "Mupirocin / موبيروسين", frequency: "مرتين يومياً", image: null },
            { name: "Omeprazole / أوميبرازول", frequency: "قبل العشاء", image: null },
            { name: "Cetirizine / سيتريزين", frequency: "في الصباح", image: null }
          ];
          
          setMedicines(extractedMedicines);
          setLoading(false);
          setStep('schedule');
        }, 2000);
      }
    }
  };

  // Function to capture image from camera
  const handleCameraCapture = () => {
    document.getElementById('fileInput').click();
  };

  // Function to reset and start over
  const handleReset = () => {
    setPrescriptionImage(null);
    setMedicines([]);
    setStep('upload');
  };

  // Function to go back to schedule view
  const handleBackToSchedule = () => {
    setStep('schedule');
  };

  // Function to remove medicine image
  const removeImage = (index) => {
    const updatedMedicines = [...medicines];
    updatedMedicines[index].image = null;
    setMedicines(updatedMedicines);
  };

  // Function to determine time category
  const determineCategory = (frequency) => {
    if (frequency.includes("صباح") || frequency.includes("Morning") || 
        frequency.includes("الفطار") || frequency.includes("breakfast")) {
      return "morning";
    } else if (frequency.includes("ظهر") || frequency.includes("Afternoon") || 
               frequency.includes("الغداء") || frequency.includes("lunch")) {
      return "afternoon";
    } else if (frequency.includes("مساء") || frequency.includes("Evening") || 
               frequency.includes("العشاء") || frequency.includes("dinner") || 
               frequency.includes("النوم") || frequency.includes("bed")) {
      return "evening";
    } else {
      return "other";
    }
  };

  // Function to determine time icon based on frequency
  const getTimeIcon = (frequency) => {
    if (frequency.includes("كل") || frequency.includes("Every")) {
      return "⏱️";
    } else if (frequency.includes("قبل") || frequency.includes("Before")) {
      return "🍽️";
    } else if (frequency.includes("بعد") || frequency.includes("After")) {
      return "☕";
    } else if (frequency.includes("عند") || frequency.includes("As needed")) {
      return "⚠️";
    } else if (frequency.includes("مرة") || frequency.includes("Once")) {
      return "1️⃣";
    } else if (frequency.includes("مرتين") || frequency.includes("Twice")) {
      return "2️⃣";
    } else if (frequency.includes("صباح") || frequency.includes("Morning")) {
      return "🌅";
    } else if (frequency.includes("ظهر") || frequency.includes("Afternoon")) {
      return "🏙️";
    } else if (frequency.includes("مساء") || frequency.includes("Evening")) {
      return "🌆";
    } else {
      return "💊";
    }
  };

  // Function to determine background color based on frequency type
  const getBackgroundColor = (frequency) => {
    const category = determineCategory(frequency);
    switch(category) {
      case "morning":
        return "bg-yellow-100";
      case "afternoon":
        return "bg-orange-100";
      case "evening":
        return "bg-indigo-100";
      default:
        return "bg-gray-100";
    }
  };

  // Filter medicines based on timing and search term
  const filteredMedicines = medicines.filter(medicine => {
    const matchesFilter = filter === 'all' || 
      (filter === 'morning' && determineCategory(medicine.frequency) === "morning") ||
      (filter === 'afternoon' && determineCategory(medicine.frequency) === "afternoon") ||
      (filter === 'evening' && determineCategory(medicine.frequency) === "evening") ||
      (filter === 'breakfast' && (medicine.frequency.includes('الفطار') || medicine.frequency.includes('breakfast'))) ||
      (filter === 'lunch' && (medicine.frequency.includes('الغداء') || medicine.frequency.includes('lunch'))) ||
      (filter === 'dinner' && (medicine.frequency.includes('العشاء') || medicine.frequency.includes('dinner'))) ||
      (filter === 'asNeeded' && (medicine.frequency.includes('عند اللزوم') || medicine.frequency.includes('As needed')));
    
    const matchesSearch = medicine.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesFilter && matchesSearch;
  });

  // Render the calendar view
  const renderCalendarView = () => (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="col-span-1">
        <h2 className="font-bold mb-2 text-center bg-yellow-200 py-2 rounded-t-lg">Morning</h2>
        <div className="border rounded-b-lg p-4 space-y-3">
          {filteredMedicines
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
                        onClick={() => removeImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => {
                        setSelectedMed(medicines.indexOf(med));
                        setShowImageUpload(true);
                      }}
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
          {filteredMedicines
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
                        onClick={() => removeImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => {
                        setSelectedMed(medicines.indexOf(med));
                        setShowImageUpload(true);
                      }}
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
          {filteredMedicines
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
                        onClick={() => removeImage(medicines.indexOf(med))}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-4 h-4 flex items-center justify-center"
                      >
                        <X size={10} />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => {
                        setSelectedMed(medicines.indexOf(med));
                        setShowImageUpload(true);
                      }}
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

  // Render the cards view
  const renderCardsView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {filteredMedicines.map((medicine, index) => (
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
                onClick={() => removeImage(index)}
                className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 w-5 h-5 flex items-center justify-center"
              >
                <X size={12} />
              </button>
            </div>
          )}
          {!medicine.image && (
            <button 
              onClick={() => {
                setSelectedMed(index);
                setShowImageUpload(true);
              }}
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

  return (
    <div className="max-w-4xl mx-auto p-4 font-sans">
      <h1 className="text-2xl font-bold mb-6 text-center">Prescription Medication Tracker</h1>
      
      {step === 'upload' && (
        <div className="text-center p-8 border-2 border-dashed border-gray-300 rounded-lg">
          <input
            type="file"
            id="fileInput"
            accept="image/*"
            className="hidden"
            onChange={handleImageUpload}
          />
          
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <button 
                onClick={handleBackToSchedule}
                className="flex items-center text-gray-600 hover:text-blue-600"
              >
                <ArrowLeft size={18} className="mr-1" />
                Back to Schedule
              </button>
              <h2 className="text-xl font-semibold">Upload Prescription Image</h2>
              <div className="w-8"></div> {/* Spacer for alignment */}
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
                onClick={handleCameraCapture}
                className="flex items-center justify-center gap-2 bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
              >
                <Camera size={20} />
                Take Photo
              </button>
            </div>
          </div>
        </div>
      )}
      
      {step === 'processing' && (
        <div className="text-center p-8 border rounded-lg">
          <div className="flex justify-between items-center mb-4">
            <button 
              onClick={() => {
                setStep('upload');
                setPrescriptionImage(null);
              }}
              className="flex items-center text-gray-600 hover:text-blue-600"
            >
              <ArrowLeft size={18} className="mr-1" />
              Back to Upload
            </button>
            <h2 className="text-xl font-semibold">Processing Prescription</h2>
            <div className="w-8"></div> {/* Spacer for alignment */}
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
      )}
      
      {step === 'schedule' && (
        <div>
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-semibold">Your Medication Schedule</h2>
            <button
              onClick={handleReset}
              className="flex items-center text-gray-600 hover:text-red-600"
            >
              <X size={18} className="mr-1" />
              New Prescription
            </button>
          </div>
          
          {/* Prescription Image Preview */}
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
          
          {/* Search and Filter */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search size={18} className="text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search medicine..."
                className="w-full pl-10 p-2 border rounded"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex gap-2 overflow-x-auto pb-1">
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('all')}
              >
                All
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'morning' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('morning')}
              >
                Morning
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'afternoon' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('afternoon')}
              >
                Afternoon
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'evening' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('evening')}
              >
                Evening
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'breakfast' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('breakfast')}
              >
                Breakfast
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'lunch' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('lunch')}
              >
                Lunch
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'dinner' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('dinner')}
              >
                Dinner
              </button>
              <button 
                className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'asNeeded' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
                onClick={() => setFilter('asNeeded')}
              >
                As Needed
              </button>
            </div>
          </div>
          
          {/* View Mode Toggle */}
          <div className="flex justify-end mb-4">
            <div className="inline-flex rounded-md shadow-sm">
              <button 
                onClick={() => setViewMode('cards')}
                className={`px-4 py-2 rounded-l-lg ${viewMode === 'cards' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
              >
                Card View
              </button>
              <button 
                onClick={() => setViewMode('calendar')}
                className={`px-4 py-2 rounded-r-lg ${viewMode === 'calendar' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
              >
                Calendar View
              </button>
            </div>
          </div>
          
          {/* Medicine Display */}
          {viewMode === 'cards' ? renderCardsView() : renderCalendarView()}
          
          {filteredMedicines.length === 0 && (
            <div className="text-center p-8 text-gray-500">
              No medicines found matching your criteria
            </div>
          )}
          
          {/* Legend for icons */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Guide:</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div className="flex items-center">
                <span className="mr-2">⏱️</span>
                <span>Every X hours</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">🍽️</span>
                <span>Before meal/bed</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">☕</span>
                <span>After meal</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">⚠️</span>
                <span>As needed</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">1️⃣</span>
                <span>Once daily</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">2️⃣</span>
                <span>Twice daily</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">🌅</span>
                <span>Morning</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">🏙️</span>
                <span>Afternoon</span>
              </div>
              <div className="flex items-center">
                <span className="mr-2">🌆</span>
                <span>Evening</span>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Image Upload Modal */}
      {showImageUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-md w-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Upload Medication Image</h3>
              <button onClick={() => setShowImageUpload(false)}>
                <X size={20} />
              </button>
            </div>
            <p className="mb-4 text-gray-600">Upload an image of the medication for visual reference</p>
            <input
              type="file"
              id="medImageInput"
              accept="image/*"
              className="hidden"
              onChange={handleImageUpload}
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
                onClick={handleCameraCapture}
                className="flex-1 flex items-center justify-center gap-2 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                <Camera size={16} />
                Camera
              </button>
            </div>
            <div className="mt-4 flex justify-center">
              <button
                onClick={() => setShowImageUpload(false)}
                className="text-gray-600 hover:text-gray-800 px-4 py-2"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PrescriptionTracker;