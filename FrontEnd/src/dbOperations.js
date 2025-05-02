// src/dbOperations.js

import axios from 'axios';

// Base URL for the JSON server
const API_URL = 'http://localhost:5000/prescriptions';

// Fetch prescriptions from the JSON server
export const fetchPrescriptions = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching prescriptions:', error);
    throw error;
  }
};

// Add a new prescription to the JSON server
export const addPrescription = async (prescriptions) => {
  try {
    if (!Array.isArray(prescriptions)) prescriptions = [prescriptions];

    const added = await Promise.all(
      prescriptions.map((prescription) =>
        axios.post(API_URL, prescription)
      )
    );

    return added.map(res => res.data);
  } catch (error) {
    console.error('Error adding prescription:', error);
    throw error;
  }
};

// You can add other DB operations like update and delete as needed.
