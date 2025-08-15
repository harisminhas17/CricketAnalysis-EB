import api from '@/lib/api';

export const fetchSuggestions = async (type: 'country' | 'state' | 'city' | 'nationality', query: string) => {
  // Example endpoints, adjust as per your backend
  let endpoint = '';
  switch (type) {
    case 'country':
      endpoint = `/suggest/countries?q=${encodeURIComponent(query)}`;
      break;
    case 'state':
      endpoint = `/suggest/states?q=${encodeURIComponent(query)}`;
      break;
    case 'city':
      endpoint = `/suggest/cities?q=${encodeURIComponent(query)}`;
      break;
    case 'nationality':
      endpoint = `/suggest/nationalities?q=${encodeURIComponent(query)}`;
      break;
    default:
      throw new Error('Invalid suggestion type');
  }
  const res = await api.get(endpoint);
  return res.data.suggestions || [];
};
