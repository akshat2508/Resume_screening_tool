// src/components/ResumeCard.jsx
import React from 'react';

const ResumeCard = ({ rank, name, score }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-bold">Rank: {rank}</h3>
      <p className="text-gray-600">Name: {name}</p>
      <p className="text-green-600 font-semibold">Score: {(score * 100).toFixed(2)}%</p>
    </div>
  );
};

export default ResumeCard;
