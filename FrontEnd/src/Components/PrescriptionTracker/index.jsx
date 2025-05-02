import React, { useState, useEffect } from 'react';
import { Camera, Upload, Calendar, Clock, Search, X, Image as ImageIcon } from 'lucide-react';
import { fetchPrescriptions } from '../../dbOperations';
import { Prev } from 'react-bootstrap/esm/PageItem';


const PrescriptionTracker = ({medicines = [], setMedicines}) => {
  const [step, setStep] = useState('schedule');
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('cards');
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [selectedMed, setSelectedMed] = useState(null);

  useEffect(() => {
    let isMounted = true;
  
    const getPrescriptions = async () => {
      try {
        const data = await fetchPrescriptions();
        if (isMounted) {
          setMedicines(data); // Replace instead of append
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error fetching prescriptions:', error);
        }
      }
    };
  
    getPrescriptions();
  
    return () => {
      isMounted = false;
    };
  }, []);
  
  console.log("medicines", medicines);
  const determineCategory = (frequency) => {
    if (frequency.includes("صباح") || frequency.includes("الفطار")) return "morning";
    if (frequency.includes("ظهر") || frequency.includes("الغداء")) return "afternoon";
    if (frequency.includes("مساء") || frequency.includes("العشاء") || frequency.includes("النوم")) return "evening";
    return "other";
  };

  const filteredMedicines = medicines.filter(med =>
    (filter === 'all' || determineCategory(med.dosage) === filter) &&
    med.medicine.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderCardsView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {filteredMedicines.map((medicine, index) => (
        <div key={index} className={`p-4 rounded-lg shadow bg-indigo-50`}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <h2 className="font-semibold">{medicine.medicine}</h2>
            </div>
          </div>
          <p className="text-indigo-700 mb-2">{medicine.dosage}</p>
        </div>
      ))}
    </div>
  );


  const renderCalendarView = () => {
    const times = ["morning", "afternoon", "evening"];
  
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {times.map((time) => {
          const medsInTime = filteredMedicines.filter(
            (med) => determineCategory(med.dosage) === time
          );
  
          if (medsInTime.length === 0) return null;
  
          return (
            <div key={time} className="col-span-1">
              <h2 className="font-bold mb-2 text-center bg-indigo-200 py-2 rounded-t-lg capitalize">
                {time}
              </h2>
              <div className="border rounded-b-lg p-4 space-y-3">
                {medsInTime.map((med, index) => (
                  <div key={index} className="p-2 bg-indigo-50 rounded border border-indigo-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{med.medicine}</p>
                        <p className="text-sm text-indigo-600">{med.dosage}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    );
  };
  
  

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
          {filteredMedicines.length === 0 ? (
              <div className="text-center text-gray-500 mt-10 text-lg">
                No prescriptions available.
              </div>
            ) : (
              viewMode === 'cards' ? renderCardsView() : renderCalendarView()
          )}

          
          </div>
      </div>
    </div>
  );
  
};

export default PrescriptionTracker;