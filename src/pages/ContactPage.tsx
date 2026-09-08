import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, MapPin, Phone, Mail, Clock, Send, CheckCircle2 } from 'lucide-react'

export function ContactPage() {
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
            <ArrowLeft size={16} /> Home
          </Link>
          <span className="font-heading text-lg font-bold text-gray-900">Contact & Outlets</span>
          <div className="w-16" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-12">
        <div className="mb-10 text-center">
          <h1 className="font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Get in Touch with SHP
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-gray-500">
            Have questions regarding table bookings, party catering, or feedback? We’d love to hear from you.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Outlet Contact Details */}
          <div className="space-y-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="font-heading text-xl font-bold text-gray-900">Main Outlet Information</h2>

            <div className="space-y-4 text-xs text-gray-700">
              <div className="flex items-start gap-3">
                <MapPin size={18} className="text-[#f47b20] shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-gray-900">SHP Restaurant - Civil Lines</p>
                  <p className="text-gray-500">Plot 14, Main Boulevard, Civil Lines, City</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Phone size={18} className="text-[#f47b20] shrink-0" />
                <span>+91 98765 43210 / 011 2345 6789</span>
              </div>

              <div className="flex items-center gap-3">
                <Mail size={18} className="text-[#f47b20] shrink-0" />
                <span>contact@shprestaurant.com</span>
              </div>

              <div className="flex items-start gap-3">
                <Clock size={18} className="text-[#f47b20] shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-gray-900">Operating Hours</p>
                  <p className="text-gray-500">Mon - Sun: 11:00 AM – 11:30 PM</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Inquiry Form */}
          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="font-heading text-xl font-bold text-gray-900 mb-4">Send Us a Message</h2>

            {submitted ? (
              <div className="text-center py-8 space-y-3">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                  <CheckCircle2 size={32} />
                </div>
                <h3 className="text-lg font-bold text-gray-900">Message Sent!</h3>
                <p className="text-xs text-gray-500">Thank you for reaching out. We will get back to you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="font-bold text-gray-700 block mb-1">Your Name</label>
                  <input
                    type="text"
                    required
                    placeholder="John Doe"
                    className="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="font-bold text-gray-700 block mb-1">Email / Phone</label>
                  <input
                    type="text"
                    required
                    placeholder="john@example.com"
                    className="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="font-bold text-gray-700 block mb-1">Message</label>
                  <textarea
                    rows={4}
                    required
                    placeholder="Write your feedback or inquiry..."
                    className="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-2 rounded-md bg-[#f47b20] py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
                >
                  <Send size={14} /> Send Inquiry
                </button>
              </form>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
