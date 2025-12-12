import { useState, useEffect } from 'react';
import { BackgroundPaths } from './components/ui/background-paths';
import { FakeNewsDetector } from './components/FakeNewsDetector';
import { VisualDetector } from './components/VisualDetector';
import { Button } from './components/ui/button';
import { Switch } from './components/ui/switch';
import { Moon, Sun, FileText, Image, ArrowLeft } from 'lucide-react';
import './index.css';

type Tab = 'landing' | 'text' | 'visual';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('landing');
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Check system preference or saved preference
    const isDark = localStorage.getItem('darkMode') === 'true' || 
      (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    setDarkMode(isDark);
    if (isDark) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode.toString());
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  if (activeTab === 'landing') {
    return (
      <div className="relative">
        {/* Dark Mode Toggle - Top Right */}
        <div className="fixed top-6 right-6 z-50 flex items-center gap-3 bg-white/80 dark:bg-slate-800/80 backdrop-blur-md px-4 py-2 rounded-full shadow-lg">
          <Sun className="h-4 w-4 text-slate-600 dark:text-slate-400" />
          <Switch checked={darkMode} onCheckedChange={toggleDarkMode} />
          <Moon className="h-4 w-4 text-slate-600 dark:text-slate-400" />
        </div>
        <BackgroundPaths
          title="Fake News Detector"
          onButtonClick={() => setActiveTab('text')}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header with Navigation */}
      <header className="sticky top-0 z-40 bg-white/80 dark:bg-slate-800/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setActiveTab('landing')}
                className="gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Home
              </Button>
              <div className="h-6 w-px bg-slate-300 dark:bg-slate-600" />
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600 dark:from-white dark:to-slate-300">
                Fake News Detector
              </h1>
            </div>

            {/* Tab Navigation */}
            <div className="flex items-center gap-2">
              <Button
                variant={activeTab === 'text' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setActiveTab('text')}
                className="gap-2"
              >
                <FileText className="h-4 w-4" />
                Text Analysis
              </Button>
              <Button
                variant={activeTab === 'visual' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setActiveTab('visual')}
                className="gap-2"
              >
                <Image className="h-4 w-4" />
                Visual Detection
              </Button>
            </div>

            {/* Dark Mode Toggle */}
            <div className="flex items-center gap-3">
              <Sun className="h-4 w-4 text-slate-600 dark:text-slate-400" />
              <Switch checked={darkMode} onCheckedChange={toggleDarkMode} />
              <Moon className="h-4 w-4 text-slate-600 dark:text-slate-400" />
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <main>
        {activeTab === 'text' && <FakeNewsDetector />}
        {activeTab === 'visual' && <VisualDetector />}
      </main>
    </div>
  );
}

export default App;
