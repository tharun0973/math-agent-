import { FiPlus } from 'react-icons/fi';

const Sidebar = ({ chatHistory, onNewChat }) => {
  return (
    <div className="w-56 bg-primary-dark h-screen flex flex-col border-r border-gray-700">
      {/* New Chat Button */}
      <div className="p-4 border-b border-gray-700">
        <button 
          onClick={onNewChat}
          className="w-full bg-primary-orange hover:bg-primary-orange-hover text-white font-semibold py-2 px-3 rounded-lg transition-colors shadow-lg flex items-center justify-center gap-2 text-sm"
        >
          <FiPlus className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* Search History */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-gray-300 text-sm font-semibold mb-3 uppercase tracking-wide">
          Search History
        </h3>
        {chatHistory.length === 0 ? (
          <p className="text-gray-500 text-xs italic">No searches yet</p>
        ) : (
          <div className="space-y-2">
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className="p-2 bg-gray-800 hover:bg-gray-700 rounded cursor-pointer transition-colors"
              >
                <p className="text-white text-xs font-medium truncate">
                  {chat.question || 'Untitled'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <p className="text-white text-sm font-semibold">Multi-Modal Agent</p>
        <p className="text-gray-400 text-xs mt-1">AI Math Assistant</p>
      </div>
    </div>
  );
};

export default Sidebar;
