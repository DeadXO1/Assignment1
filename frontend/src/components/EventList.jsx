import { useState, useEffect } from 'react';
import EventCard from './EventCard';
import SearchFilter from './SearchFilter';
import { fetchEvents } from '../services/api';

/**
 * EventList component displays a list of events with search and filter capabilities.
 */
export default function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    search: '',
    date_from: '',
    date_to: '',
    source: '',
    page: 1,
    page_size: 20,
  });
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    page_size: 20,
  });
  
  useEffect(() => {
    loadEvents();
  }, [filters]);
  
  // Auto-refresh events every 5 minutes to show newly scraped events
  useEffect(() => {
    const interval = setInterval(() => {
      loadEvents();
    }, 5 * 60 * 1000); // 5 minutes
    
    return () => clearInterval(interval);
  }, [filters]);
  
  const loadEvents = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await fetchEvents(filters);
      setEvents(data.events);
      setPagination({
        total: data.total,
        page: data.page,
        page_size: data.page_size,
      });
    } catch (err) {
      setError('Failed to load events. Please try again later.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters, page: 1 });
  };
  
  const handlePageChange = (newPage) => {
    setFilters({ ...filters, page: newPage });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  const totalPages = Math.ceil(pagination.total / pagination.page_size);
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Sydney Events</h1>
          <p className="mt-2 text-gray-600">Discover what's happening in Sydney</p>
        </div>
      </header>
      
      {/* Search and Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <SearchFilter
          filters={filters}
          onFilterChange={handleFilterChange}
        />
      </div>
      
      {/* Events Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center max-w-2xl mx-auto">
            <div className="mb-4">
              <svg className="w-16 h-16 text-red-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-red-900 mb-2">Connection Error</h3>
            <p className="text-red-700 mb-4">
              {error.includes('Failed to fetch') || error.includes('ERR_CONNECTION_REFUSED')
                ? "Cannot connect to the backend server. Please make sure the backend is running on http://localhost:8000"
                : error}
            </p>
            <div className="bg-white rounded p-4 text-left text-sm text-gray-700 mb-4">
              <p className="font-semibold mb-2">To start the backend:</p>
              <ol className="list-decimal list-inside space-y-1">
                <li>Open a new terminal/command prompt</li>
                <li>Navigate to the backend directory: <code className="bg-gray-100 px-1 rounded">cd backend</code></li>
                <li>Activate virtual environment: <code className="bg-gray-100 px-1 rounded">venv\Scripts\activate</code> (Windows) or <code className="bg-gray-100 px-1 rounded">source venv/bin/activate</code> (Mac/Linux)</li>
                <li>Start the server: <code className="bg-gray-100 px-1 rounded">python -m app.main</code></li>
              </ol>
            </div>
            <button
              onClick={loadEvents}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        ) : events.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-600 text-lg">No events found. Try adjusting your filters.</p>
          </div>
        ) : (
          <>
            <div className="mb-6 text-gray-600">
              Showing {events.length} of {pagination.total} events
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
            
            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex justify-center items-center gap-2">
                <button
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page === 1}
                  className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Previous
                </button>
                
                <span className="px-4 py-2 text-gray-700">
                  Page {pagination.page} of {totalPages}
                </span>
                
                <button
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page >= totalPages}
                  className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

