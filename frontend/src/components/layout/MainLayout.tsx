import { Outlet, Link } from 'react-router-dom';

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="gradient-bg text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span className="text-xl font-bold">Legal Doc Generator</span>
            </Link>
            <nav className="hidden md:flex items-center space-x-6">
              <Link to="/" className="hover:text-white/80 transition-colors">Home</Link>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="hover:text-white/80 transition-colors">
                GitHub
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-auto">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <p className="text-gray-400">
              Legal Document Generator - Generate Privacy Policies, Terms of Service, and more.
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Built with FastAPI + React
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
