export const determineCategory = (frequency) => {
    if (frequency.includes("صباح") || frequency.includes("Morning") || 
        frequency.includes("الفطار") || frequency.includes("breakfast")) {
      return "morning";
    } else if (frequency.includes("ظهر") || frequency.includes("Afternoon") || 
               frequency.includes("الغداء") || frequency.includes("lunch")) {
      return "afternoon";
    } else if (frequency.includes("مساء") || frequency.includes("Evening") || 
               frequency.includes("العشاء") || frequency.includes("dinner") || 
               frequency.includes("النوم") || frequency.includes("bed")) {
      return "evening";
    } else {
      return "other";
    }
  };
  
  export const getTimeIcon = (frequency) => {
    if (frequency.includes("كل") || frequency.includes("Every")) {
      return "⏱️";
    } else if (frequency.includes("قبل") || frequency.includes("Before")) {
      return "🍽️";
    } else if (frequency.includes("بعد") || frequency.includes("After")) {
      return "☕";
    } else if (frequency.includes("عند") || frequency.includes("As needed")) {
      return "⚠️";
    } else if (frequency.includes("مرة") || frequency.includes("Once")) {
      return "1️⃣";
    } else if (frequency.includes("مرتين") || frequency.includes("Twice")) {
      return "2️⃣";
    } else if (frequency.includes("صباح") || frequency.includes("Morning")) {
      return "🌅";
    } else if (frequency.includes("ظهر") || frequency.includes("Afternoon")) {
      return "🏙️";
    } else if (frequency.includes("مساء") || frequency.includes("Evening")) {
      return "🌆";
    } else {
      return "💊";
    }
  };
  
  export const getBackgroundColor = (frequency) => {
    const category = determineCategory(frequency);
    switch(category) {
      case "morning":
        return "bg-yellow-100";
      case "afternoon":
        return "bg-orange-100";
      case "evening":
        return "bg-indigo-100";
      default:
        return "bg-gray-100";
    }
  };