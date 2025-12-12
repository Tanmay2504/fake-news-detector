import { useState } from 'react';
import { BackgroundPaths } from './components/ui/background-paths';
import { FakeNewsDetector } from './components/FakeNewsDetector';
import './index.css';

function App() {
  const [showDetector, setShowDetector] = useState(false);

  if (showDetector) {
    return <FakeNewsDetector />;
  }

  return (
    <BackgroundPaths
      title="Fake News Detector"
      onButtonClick={() => setShowDetector(true)}
    />
  );
}

export default App;
