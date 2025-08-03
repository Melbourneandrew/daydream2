import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "@/components/Navigation";
import NewDreamView from "@/components/views/NewDreamView";
import DreamView from "@/components/views/DreamView";
import AboutView from "@/components/views/AboutView";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<AboutView />} />
            <Route path="/about" element={<AboutView />} />
            <Route path="/new" element={<NewDreamView />} />
            <Route path="/dream/:dreamId" element={<DreamView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
