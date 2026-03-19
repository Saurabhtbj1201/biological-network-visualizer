import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState, AppDispatch } from './store';
import { FileUploadPanel } from './components/FileUploadPanel';

function App() {
  const dispatch = useDispatch<AppDispatch>();
  const networks = useSelector((state: RootState) => state.networks);
  const currentNetwork = networks.currentNetworkId ? networks.networks[networks.currentNetworkId] : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">NetworkInsight</h1>
          <p className="text-gray-600 mt-1">AI-Assisted Analysis and Visualization of Biological Networks</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {!currentNetwork ? (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Get Started</h2>
            <FileUploadPanel />

            {Object.keys(networks.networks).length > 0 && (
              <div className="mt-12">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Networks</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.values(networks.networks).map((network) => (
                    <div key={network.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-lg transition-shadow">
                      <h4 className="font-semibold text-gray-900">{network.name}</h4>
                      <p className="text-sm text-gray-600 mt-2">
                        Nodes: {network.nodes_count} | Edges: {network.edges_count}
                      </p>
                      <button
                        onClick={() => {
                          // TODO: Load network details
                        }}
                        className="mt-4 w-full bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition-colors"
                      >
                        Open
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">{currentNetwork.name}</h2>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600">Nodes</p>
                <p className="text-2xl font-bold text-blue-600">{currentNetwork.nodes_count}</p>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-600">Edges</p>
                <p className="text-2xl font-bold text-green-600">{currentNetwork.edges_count}</p>
              </div>
            </div>
            <p className="text-gray-600 text-sm">Status: {currentNetwork.status}</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-gray-600 text-sm">
          <p>NetworkInsight • GSoC 2026 Project • Built for NRNB</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
