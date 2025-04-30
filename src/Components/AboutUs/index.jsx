import React from "react";
import { FaLinkedin, FaGithub } from "react-icons/fa";
import { MdEmail } from "react-icons/md";

const teamMembers = [
    {
      name: "Habiba Yousri",
      role: "Team Leader, AI Engineer",
      linkedin: "https://www.linkedin.com/in/habiba-yousri/",
      github: "https://github.com/HabibaYossre",
      email: "habibayousri46@gmail.com",
    },
    {
      name: "Mohammed Mostafa",
      role: "AI Engineer",
      linkedin: "https://www.linkedin.com/in/mohammed-mostafa237/",
      github: "https://github.com/Mohammed2372",
      email: "mohammedmostafa2372002@gmail.com",
    },
    {
        name: "Haneen Akram",
        role: "AI Engineer",
        linkedin: "https://www.linkedin.com/in/haneen-akram/",
        github: "https://github.com/haneenakram",
        email: "Haneenakram3040@gmail.com",
    },
    {
      name: "Shrouk Aboalela",
      role: "AI Engineer",
      linkedin: "https://linkedin.com/in/noura-alaa",
      github: "https://github.com/noura-alaa",
      email: "shrouk@example.com",
    },
    {
      name: "Renad Hossam",
      role: "Full Stack Engineer",
      linkedin: "https://www.linkedin.com/in/renad-hossam-940576198/",
      github: "https://github.com/Renad03",
      email: "renad03emara@gmail.com",
    },
  ];

  
const AboutUs = () => {
  return (
    <div className="mt-20 px-4 w-full">
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        <h1 className="text-3xl font-bold text-indigo-800 text-center">About Us</h1>
        <div className="text-lg text-gray-700 space-y-4">
          <p>
            Welcome to the Pen to Pill! Our mission is to simplify the
            management of your medications and prescriptions. We believe in providing
            a user-friendly platform that helps you stay on top of your health.
          </p>
          <p>
            Our team consists of tech experts, all
            dedicated to creating a seamless experience for users like you. Whether
            you're managing a single prescription or multiple medications, our goal is
            to make your experience easier and more efficient.
          </p>

          
          <div className="mt-20 px-4">
      <div className="mx-auto max-w-4xl">
        <h2 className="text-3xl font-bold text-indigo-800 mb-8 text-center">Meet the Team</h2>
        <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {teamMembers.map((member) => (
            <div key={member.name} className="bg- shadow-md rounded-lg p-6 text-center">
              <h3 className="text-xl font-semibold text-indigo-800">{member.name}</h3>
              <p className="text-gray-600 mb-4">{member.role}</p>
              <div className="flex justify-center space-x-4">
                <a href={member.linkedin} target="_blank" rel="noopener noreferrer">
                  <FaLinkedin className="text-indigo-600 hover:text-indigo-800 w-6 h-6" />
                </a>
                <a href={member.github} target="_blank" rel="noopener noreferrer">
                  <FaGithub className="text-gray-800 hover:text-black w-6 h-6" />
                </a>
                <a href={`mailto:${member.email}`}>
                  <MdEmail className="text-red-600 hover:text-red-800 w-6 h-6" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>


        </div>
      </div>
    </div>
  );
};

export default AboutUs;
