import React from 'react';
import { Link } from 'react-router-dom';
import  Button  from '../Button';
import  Card  from '../Card';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* Hero Section */}
      <section className="bg-blue-900 py-5 px-6 text-center">
        <h1 className="text-4xl font-bold mb-4 text-zinc-50">From Pen to Pill</h1>
        <p className="text-lg mb-6 text-zinc-50"> We'll create a smart schedule to keep you on track.</p>
        
      </section>

      {/* How It Works */}
      <section className="py-16 px-6">
        <h2 className="text-2xl font-semibold text-center mb-10">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <Card className="p-6">
            <h3 className="font-semibold text-lg mb-2">1. Upload</h3>
            <p>Snap a photo of your prescription using your phone or upload a file.</p>
          </Card>
          <Card className="p-6">
            <h3 className="font-semibold text-lg mb-2">2. AI Analyzes</h3>
            <p>Our system extracts medicines and dosage instructions using AI.</p>
          </Card>
          <Card className="p-6">
            <h3 className="font-semibold text-lg mb-2">3. Get Schedule</h3>
            <p>Receive a personalized medication schedule with reminders.</p>
          </Card>
        </div>
      </section>


      {/* Benefits */}
      <section className="py-16 px-6">
        <h2 className="text-2xl font-semibold text-center mb-10">Why Use P2P?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="p-6">⏰ Never miss a dose again</Card>
          <Card className="p-6">📋 Automatically organized schedule</Card>
          <Card className="p-6">👵🏽 Designed for all ages</Card>
          <Card className="p-6">🧠 AI-assisted medication extraction</Card>
          <Card className="p-6">🔒 Secure & private</Card>
        </div>
      </section>

      {/* Navigation Links */}
      <section className="bg-green-50 py-10 px-6 text-center">
        <h2 className="text-xl font-semibold mb-6">Get Started</h2>
        <div className="space-x-4">
          <Link to="/upload">
            <Button className="bg-green-600 text-white hover:bg-green-700">Upload Prescription</Button>
          </Link>
          <Link to="/schedule">
            <Button variant="outline">View My Schedule</Button>
          </Link>
          <Link to="/add-medicine">
            <Button variant="outline">Add Medication Manually</Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
