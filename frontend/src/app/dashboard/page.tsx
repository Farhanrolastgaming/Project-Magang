"use client";

import { useAuth } from "@/context/AuthContext";
import { Globe, BarChart3, Palette, ArrowRight, Sparkles } from "lucide-react";
import Link from "next/link";

export default function DashboardHome() {
  const { user } = useAuth();

  const features = [
    {
      title: "WP Automation",
      description: "Generate artikel SEO dan posting ke semua situs WordPress Anda secara otomatis.",
      icon: Globe,
      href: "/dashboard/wp-automation",
      color: "indigo",
      gradient: "from-indigo-500/20 to-blue-500/20",
      iconColor: "text-indigo-400",
      borderHover: "hover:border-indigo-500/40",
    },
    {
      title: "Analisis & Performance",
      description: "Pantau statistik artikel, tren, dan performa SEO di setiap akun WordPress.",
      icon: BarChart3,
      href: "/dashboard/analytics",
      color: "pink",
      gradient: "from-pink-500/20 to-rose-500/20",
      iconColor: "text-pink-400",
      borderHover: "hover:border-pink-500/40",
    },
    {
      title: "Tool UI (Theme Modifier)",
      description: "Ubah tampilan website WordPress Anda menggunakan prompt AI secara instan.",
      icon: Palette,
      href: "/dashboard/tool-ui",
      color: "purple",
      gradient: "from-purple-500/20 to-violet-500/20",
      iconColor: "text-purple-400",
      borderHover: "hover:border-purple-500/40",
    },
  ];

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Welcome */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/20">
            <Sparkles className="w-5 h-5 text-purple-400" />
          </div>
          <h1 className="text-3xl font-bold text-white">
            Welcome, {user?.name || "User"}!
          </h1>
        </div>
        <p className="text-neutral-500 ml-12">
          Choose a feature below to get started with your WordPress automation.
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        {features.map((feature) => (
          <Link
            key={feature.href}
            href={feature.href}
            className={`group relative p-6 rounded-2xl bg-white/[0.02] border border-white/5 ${feature.borderHover} transition-all hover:shadow-2xl overflow-hidden`}
          >
            {/* Background gradient */}
            <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
            
            <div className="relative z-10">
              <feature.icon className={`w-10 h-10 ${feature.iconColor} mb-4 group-hover:scale-110 transition-transform`} />
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-neutral-400 mb-4 leading-relaxed">{feature.description}</p>
              <span className="inline-flex items-center gap-1 text-xs font-medium text-neutral-500 group-hover:text-white transition-colors">
                Open <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
              </span>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Stats placeholder */}
      <div className="mt-10 grid grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/5">
          <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Connected Sites</p>
          <p className="text-3xl font-bold text-white">0 <span className="text-sm font-normal text-neutral-500">/ 10</span></p>
        </div>
        <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/5">
          <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Articles Generated</p>
          <p className="text-3xl font-bold text-white">0</p>
        </div>
        <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/5">
          <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Published Today</p>
          <p className="text-3xl font-bold text-white">0</p>
        </div>
      </div>
    </div>
  );
}
