import React from 'react';
import { Search } from 'lucide-react';

const FilterControls = ({
  filter,
  searchTerm,
  viewMode,
  onSetFilter,
  onSetSearchTerm,
  onSetViewMode
}) => {
  return (
    <>
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
            onChange={(e) => onSetSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex gap-2 overflow-x-auto pb-1">
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('all')}
          >
            All
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'morning' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('morning')}
          >
            Morning
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'afternoon' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('afternoon')}
          >
            Afternoon
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'evening' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('evening')}
          >
            Evening
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'breakfast' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('breakfast')}
          >
            Breakfast
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'lunch' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('lunch')}
          >
            Lunch
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'dinner' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('dinner')}
          >
            Dinner
          </button>
          <button 
            className={`px-3 py-1 rounded whitespace-nowrap ${filter === 'asNeeded' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => onSetFilter('asNeeded')}
          >
            As Needed
          </button>
        </div>
      </div>
      
      <div className="flex justify-end mb-4">
        <div className="inline-flex rounded-md shadow-sm">
          <button 
            onClick={() => onSetViewMode('cards')}
            className={`px-4 py-2 rounded-l-lg ${viewMode === 'cards' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Card View
          </button>
          <button 
            onClick={() => onSetViewMode('calendar')}
            className={`px-4 py-2 rounded-r-lg ${viewMode === 'calendar' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Calendar View
          </button>
        </div>
      </div>
    </>
  );
};

export default FilterControls;