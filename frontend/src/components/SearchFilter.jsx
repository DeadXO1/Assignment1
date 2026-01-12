/**
 * SearchFilter component for filtering events by search term, date range, and source.
 */
export default function SearchFilter({ filters, onFilterChange }) {
  const handleSearchChange = (e) => {
    onFilterChange({ search: e.target.value });
  };
  
  const handleDateFromChange = (e) => {
    onFilterChange({ date_from: e.target.value });
  };
  
  const handleDateToChange = (e) => {
    onFilterChange({ date_to: e.target.value });
  };
  
  const handleSourceChange = (e) => {
    onFilterChange({ source: e.target.value });
  };
  
  const handleClearFilters = () => {
    onFilterChange({
      search: '',
      date_from: '',
      date_to: '',
      source: '',
    });
    // Also clear the input fields visually
    document.getElementById('search')?.value && (document.getElementById('search').value = '');
    document.getElementById('date_from')?.value && (document.getElementById('date_from').value = '');
    document.getElementById('date_to')?.value && (document.getElementById('date_to').value = '');
    document.getElementById('source')?.value && (document.getElementById('source').value = '');
  };
  
  const hasActiveFilters = filters.search || filters.date_from || filters.date_to || filters.source;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <input
            type="text"
            id="search"
            value={filters.search}
            onChange={handleSearchChange}
            placeholder="Search events..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Date From */}
        <div>
          <label htmlFor="date_from" className="block text-sm font-medium text-gray-700 mb-2">
            From Date
          </label>
          <input
            type="date"
            id="date_from"
            value={filters.date_from}
            onChange={handleDateFromChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Date To */}
        <div>
          <label htmlFor="date_to" className="block text-sm font-medium text-gray-700 mb-2">
            To Date
          </label>
          <input
            type="date"
            id="date_to"
            value={filters.date_to}
            onChange={handleDateToChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Source */}
        <div>
          <label htmlFor="source" className="block text-sm font-medium text-gray-700 mb-2">
            Source
          </label>
          <select
            id="source"
            value={filters.source}
            onChange={handleSourceChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Sources</option>
            <option value="eventbrite">Eventbrite</option>
            <option value="meetup">Meetup</option>
            <option value="timeout">TimeOut</option>
          </select>
        </div>
      </div>
      
      {/* Clear Filters */}
      {hasActiveFilters && (
        <div className="mt-4">
          <button
            onClick={handleClearFilters}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}

