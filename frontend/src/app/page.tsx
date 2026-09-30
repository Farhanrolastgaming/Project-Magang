import Link from "next/link";
import { ArrowRight, Sparkles, LayoutDashboard, LineChart, Globe } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-neutral-950 font-sans text-neutral-50 overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">Gen-AutoPress</span>
          </div>
          
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-400">
            <Link href="#features" className="hover:text-white transition-colors">Features</Link>
            <Link href="#how-it-works" className="hover:text-white transition-colors">How it Works</Link>
            <Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-medium hover:text-white transition-colors">
              Sign In
            </Link>
            <Link 
              href="/register" 
              className="px-5 py-2.5 rounded-full bg-white text-black text-sm font-semibold hover:bg-neutral-200 transition-all flex items-center gap-2"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6">
        {/* Background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="relative max-w-5xl mx-auto text-center flex flex-col items-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 mb-8">
            <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-sm font-medium text-neutral-300">v2.0 Early Access is Live</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-8 leading-[1.1] max-w-4xl">
            Scale Your WordPress <br className="hidden md:block"/> 
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              Content with AI
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-neutral-400 max-w-2xl mb-12 leading-relaxed">
            Automate SEO-optimized articles, manage multiple WordPress sites, and track performance analytics—all in one powerful, multi-tenant platform.
          </p>

          <div className="flex flex-col sm:flex-row items-center gap-4">
            <Link 
              href="/register"
              className="px-8 py-4 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold text-lg hover:shadow-[0_0_40px_-10px_rgba(124,58,237,0.5)] hover:scale-105 transition-all w-full sm:w-auto flex items-center justify-center gap-2"
            >
              Start Automating
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              href="#demo"
              className="px-8 py-4 rounded-full border border-white/20 bg-white/5 hover:bg-white/10 text-white font-semibold text-lg transition-all w-full sm:w-auto"
            >
              View Analysis
            </Link>
          </div>
        </div>
      </main>

      {/* Features Preview */}
      <section className="border-t border-white/10 bg-neutral-950/50 py-24 relative z-10 px-6">
        <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-8">
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 hover:border-indigo-500/50 transition-colors group">
            <Globe className="w-10 h-10 text-indigo-400 mb-6 group-hover:scale-110 transition-transform" />
            <h3 className="text-xl font-semibold mb-3">WP Automation (Multi-Site)</h3>
            <p className="text-neutral-400">Hubungkan hingga 10 akun WordPress. Generate artikel SEO dengan AI dan posting ke semua situs Anda secara otomatis hanya dengan 1 klik.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 hover:border-pink-500/50 transition-colors group">
            <LineChart className="w-10 h-10 text-pink-400 mb-6 group-hover:scale-110 transition-transform" />
            <h3 className="text-xl font-semibold mb-3">Analisis & Performance</h3>
            <p className="text-neutral-400">Pantau statistik lengkap dari artikel di setiap akun Anda. Lihat tren, performa SEO, dan artikel top trending dalam satu dashboard pintar.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 hover:border-purple-500/50 transition-colors group">
            <LayoutDashboard className="w-10 h-10 text-purple-400 mb-6 group-hover:scale-110 transition-transform" />
            <h3 className="text-xl font-semibold mb-3">Tool UI (Theme Modifier)</h3>
            <p className="text-neutral-400">Ubah tatanan letak website WordPress Anda menggunakan *prompt* AI. Didukung teknologi MCP dan REST API untuk kustomisasi tema secara instan.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
