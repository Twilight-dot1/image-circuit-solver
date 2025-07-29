// File: App.jsx
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, Zap } from 'lucide-react';

export default function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      // Normally you'd send to backend here
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    // Simulate API call to analyze image
    setTimeout(() => {
      setResult({
        totalResistance: "8.5 Ω",
        current: "1.2 A",
        voltage: "10.2 V",
      });
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <header className="text-center mb-10">
        <h1 className="text-4xl font-bold text-neon-green">Image-Based Circuit Solver</h1>
        <p className="text-gray-400">Upload a hand-drawn or printed circuit diagram to analyze it.</p>
      </header>

      <div className="max-w-3xl mx-auto grid gap-6">
        <Card className="bg-gray-800 border border-neon-green">
          <CardContent className="p-6">
            <label className="block mb-4 text-lg font-medium">Upload Circuit Image</label>
            <input type="file" accept="image/*" onChange={handleUpload} className="mb-4" />
            {image && <img src={image} alt="Uploaded" className="rounded-lg shadow-lg mb-4" />}
            <Button onClick={handleAnalyze} className="bg-neon-green hover:bg-neon-green/80 text-black">
              <Zap className="mr-2 h-4 w-4" /> Analyze
            </Button>
          </CardContent>
        </Card>

        {result && (
          <Card className="bg-gray-800 border border-blue-400">
            <CardContent className="p-6">
              <h2 className="text-2xl mb-4 font-semibold text-blue-300">Analysis Result</h2>
              <p>Total Resistance: <span className="text-neon-green">{result.totalResistance}</span></p>
              <p>Current: <span className="text-neon-green">{result.current}</span></p>
              <p>Voltage: <span className="text-neon-green">{result.voltage}</span></p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
