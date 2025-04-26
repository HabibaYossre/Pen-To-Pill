import { useState } from 'react';
import { determineCategory } from '../utils/medicineUtils';

const useMedicine = () => {
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
  
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

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

  const removeImage = (index) => {
    const updatedMedicines = [...medicines];
    updatedMedicines[index].image = null;
    setMedicines(updatedMedicines);
  };

  return {
    medicines,
    filter,
    searchTerm,
    filteredMedicines,
    setFilter,
    setSearchTerm,
    setMedicines,
    removeImage
  };
};

export default useMedicine;