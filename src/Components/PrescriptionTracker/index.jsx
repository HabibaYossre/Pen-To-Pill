import React, { useState } from 'react';
import { Camera, Upload, Calendar, Clock, Search, X, Image as ImageIcon } from 'lucide-react';

const PrescriptionTracker = () => {
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

  const handleImageUpload = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const imageUrl = URL.createObjectURL(file);
      if (showImageUpload && selectedMed !== null) {
        const updatedMedicines = [...medicines];
        updatedMedicines[selectedMed].image = imageUrl;
        setMedicines(updatedMedicines);
        setShowImageUpload(false);
        setSelectedMed(null);
      } else {
        setPrescriptionImage(imageUrl);
        setStep('processing');
        setLoading(true);
        setTimeout(() => {
          setMedicines([
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
          setLoading(false);
          setStep('schedule');
        }, 2000);
      }
    }
  };

  const determineCategory = (frequency) => {
    if (frequency.includes("صباح") || frequency.includes("الفطار")) return "morning";
    if (frequency.includes("ظهر") || frequency.includes("الغداء")) return "afternoon";
    if (frequency.includes("مساء") || frequency.includes("العشاء") || frequency.includes("النوم")) return "evening";
    return "other";
  };

  const getTimeIcon = (frequency) => {
    if (frequency.includes("كل")) return "⏱️";
    if (frequency.includes("قبل")) return "🍽️";
    if (frequency.includes("بعد")) return "☕";
    if (frequency.includes("عند")) return "⚠️";
    if (frequency.includes("مرة")) return "1️⃣";
    if (frequency.includes("مرتين")) return "2️⃣";
    if (frequency.includes("صباح")) return "🌅";
    if (frequency.includes("ظهر")) return "🏙️";
    if (frequency.includes("مساء")) return "🌆";
    return "💊";
  };

  const filteredMedicines = medicines.filter(med =>
    (filter === 'all' || determineCategory(med.frequency) === filter) &&
    med.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderCardsView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {filteredMedicines.map((medicine, index) => (
        <div key={index} className={`p-4 rounded-lg shadow bg-indigo-50`}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <span className="text-2xl mr-2">{getTimeIcon(medicine.frequency)}</span>
              <h2 className="font-semibold">{medicine.name}</h2>
            </div>
          </div>
          <p className="text-indigo-700 mb-2">{medicine.frequency}</p>
        </div>
      ))}
    </div>
  );

  const renderCalendarView = () => (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {["morning", "afternoon", "evening"].map(time => (
        <div key={time} className="col-span-1">
          <h2 className="font-bold mb-2 text-center bg-indigo-200 py-2 rounded-t-lg capitalize">{time}</h2>
          <div className="border rounded-b-lg p-4 space-y-3">
            {filteredMedicines
              .filter(med => determineCategory(med.frequency) === time)
              .map((med, index) => (
                <div key={index} className="p-2 bg-indigo-50 rounded border border-indigo-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{med.name}</p>
                      <p className="text-sm text-indigo-600">{med.frequency}</p>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="mt-20 px-4 w-full">
      <div className="max-w-4xl mx-auto">
        <div className="p-6 space-y-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-indigo-800">Prescription Tracker</h1>
            <button
              className="bg-indigo-500 text-white px-3 py-1 rounded"
              onClick={() => setViewMode(viewMode === 'cards' ? 'calendar' : 'cards')}
            >
              {viewMode === 'cards' ? <Calendar className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
            </button>
          </div>
  
          <div className="flex items-center space-x-2">
            <Search className="text-indigo-500" />
            <input
              type="text"
              placeholder="Search medicine"
              className="border px-3 py-1 rounded w-full"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
  
          {/* Add this filter bar below the search input */}
          <div className="flex gap-2 my-4">
            {["all", "morning", "afternoon", "evening"].map((cat) => (
              <button
                key={cat}
                onClick={() => setFilter(cat)}
                className={`px-3 py-1 rounded-full border ${
                  filter === cat ? "bg-indigo-600 text-white" : "bg-white text-indigo-600 border-indigo-300"
                }`}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>
  
          {showImageUpload && (
            <div className="flex items-center space-x-2">
              <input type="file" accept="image/*" onChange={handleImageUpload} />
              <button onClick={() => setShowImageUpload(false)} className="text-red-600">
                <X className="w-5 h-5" />
              </button>
            </div>
          )}
  
          {loading ? (
            <div className="text-center text-lg font-medium text-indigo-600">Processing Prescription Image...</div>
          ) : viewMode === 'cards' ? renderCardsView() : renderCalendarView()}
        </div>
      </div>
    </div>
  );
  
};

export default PrescriptionTracker;
