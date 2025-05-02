import React from 'react';
const Button = ({ children, className = '', variant = 'default', ...props }) => {
  const baseStyle = 'px-4 py-2 rounded font-semibold transition-colors';
  let variantStyle = '';

  switch (variant) {
    case 'outline':
      variantStyle = 'border border-gray-500 text-gray-800 hover:bg-gray-100';
      break;
    case 'default':
    default:
      variantStyle = 'bg-green-600 text-white hover:bg-green-700';
      break;
  }

  return (
    <button
      className={`${baseStyle} ${variantStyle} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;

