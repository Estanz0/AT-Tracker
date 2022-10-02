import { useState, useEffect } from 'react';

export default function useWindowDimensions() {

  const [width, setWidth]   = useState(window.clientWidth);
  const [height, setHeight] = useState(window.innerHeight);

  const updateDimensions = () => {
      setWidth(window.clientWidth);
      setHeight(window.innerHeight);
  }

  useEffect(() => {
      window.addEventListener("resize", updateDimensions);
      return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  return {height, width};
}