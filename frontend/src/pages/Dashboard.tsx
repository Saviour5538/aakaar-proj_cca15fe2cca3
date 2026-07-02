import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/client';

interface ResourceCounts {
  documents: number;
  conversations: number;
}

interface RecentDocument {
  id: string;
  name: string;
  uploaded_at: string;
}

interface RecentConversation {
  id: string;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [counts, setCounts] = useState<ResourceCounts | null>(null);
  const [recentDocuments, setRecentDocuments] = useState<RecentDocument[]>([]);
  const [recentConversations, setRecentConversations] = useState<RecentConversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [documentsResponse, conversationsResponse] = await Promise.all([
          axios.get('/api/documents'),
          axios.get('/api/conversations'),
        ]);

        setCounts({
          documents: documentsResponse.data.length,
          conversations: conversationsResponse.data.length,
        });

        setRecentDocuments(documentsResponse.data.slice(0, 5));
        setRecentConversations(conversationsResponse.data.slice(0, 5));
      } catch (err: any) {
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleNewChatClick = () => {
    navigate('/chat');
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-lg font-semibold">Documents</h2>
          <p className="text-2xl font-bold">{counts?.documents || 0}</p>
        </div>
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-lg font-semibold">Conversations</h2>
          <p className="text-2xl font-bold">{counts?.conversations || 0}</p>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Recent Documents</h2>
        <div className="bg-white shadow rounded-lg p-4">
          {recentDocuments.length > 0 ? (
            <ul>
              {recentDocuments.map((doc) => (
                <li key={doc.id} className="border-b last:border-b-0 py-2">
                  <span className="font-medium">{doc.name}</span>
                  <span className="text-sm text-gray-500 ml-2">
                    {new Date(doc.uploaded_at).toLocaleDateString()}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No recent documents.</p>
          )}
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Recent Conversations</h2>
        <div className="bg-white shadow rounded-lg p-4">
          {recentConversations.length > 0 ? (
            <ul>
              {recentConversations.map((conv) => (
                <li key={conv.id} className="border-b last:border-b-0 py-2">
                  <span className="font-medium">Conversation ID: {conv.id}</span>
                  <span className="text-sm text-gray-500 ml-2">
                    {new Date(conv.created_at).toLocaleDateString()}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No recent conversations.</p>
          )}
        </div>
      </div>

      <div className="flex gap-4">
        <button
          onClick={handleUploadClick}
          className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
        >
          Upload Document
        </button>
        <button
          onClick={handleNewChatClick}
          className="bg-green-500 text-white px-4 py-2 rounded shadow hover:bg-green-600"
        >
          Start New Chat
        </button>
      </div>
    </div>
  );
};

export default Dashboard;