import React, { useState, useRef } from 'react';
import { Upload } from 'lucide-react';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../store';
import { setLoading, addNetwork, setError } from '../store/networkSlice';
import { apiClient } from '../api/client';

export const FileUploadPanel: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [networkName, setNetworkName] = useState('');

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleFileSelect = async (file: File) => {
    dispatch(setLoading(true));
    try {
      const result = await apiClient.uploadNetwork(
        file,
        networkName || file.name,
        { source: 'NetworkInsight', upload_date: new Date().toISOString() }
      );

      dispatch(
        addNetwork({
          id: result.network_id,
          name: networkName || file.name,
          format: file.name.split('.').pop() || 'unknown',
          nodes_count: result.nodes_count,
          edges_count: result.edges_count,
          created_at: new Date().toISOString(),
          status: 'ready',
        })
      );

      setNetworkName('');
      alert(`Network uploaded successfully! ${result.nodes_count} nodes, ${result.edges_count} edges`);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Upload failed';
      dispatch(setError(message));
      alert(`Error uploading network: ${message}`);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Network Name (optional)</label>
        <input
          type="text"
          value={networkName}
          onChange={(e) => setNetworkName(e.target.value)}
          placeholder="Enter network name"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`flex flex-col items-center justify-center w-full p-10 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'
        }`}
      >
        <Upload className="w-12 h-12 text-gray-400 mb-2" />
        <p className="text-lg font-medium text-gray-700">Drag and drop your network file</p>
        <p className="text-sm text-gray-500 mt-1">or click to select</p>
        <p className="text-xs text-gray-400 mt-2">Supported: SIF, JSON, CSV, TSV</p>
      </div>

      <input ref={fileInputRef} type="file" onChange={handleFileInput} className="hidden" accept=".sif,.json,.csv,.tsv,.txt" />
    </div>
  );
};
