import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Calendar, Clock, Users, Sparkles, CheckCircle2 } from 'lucide-react'

export function BookingPage() {
  const [guests, setGuests] = useState(2)
  const [date, setDate] = useState('2026-09-10')
  const [timeSlot, setTimeSlot] = useState('19:30')
  const [seatingZone, setSeatingZone] = useState('Main Dining')
  const [specialRequest, setSpecialRequest] = useState('')
  const [isSubmitted, setIsSubmitted] = useState(false)

  const timeSlots = ['12:30 PM', '01:30 PM', '07:00 PM', '07:30 PM', '08:15 PM', '09:00 PM']
  const seatingOptions = [
    { name: 'Main Dining', desc: 'Warm ambiance with live kitchen view' },
    { name: 'Rooftop Terrace', desc: 'Open sky dining with city skyline view' },
    { name: 'Private VIP Booth', desc: 'Secluded cozy seating for special occasions' },
  ]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Top Header */}
      <header className="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
            <ArrowLeft size={16} /> Home
          </Link>
          <span className="font-heading text-lg font-bold text-gray-900">Table Reservation</span>
          <div className="w-16" />
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-12">
        <div className="mb-10 text-center">
          <span className="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
            <Sparkles size={14} /> Reserve Your Table
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Book a Table at SHP
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-gray-500">
            Enjoy delicious food and cozy hospitality. Instant table confirmation.
          </p>
        </div>

        {isSubmitted ? (
          <div className="rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-lg">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
              <CheckCircle2 size={40} />
            </div>
            <h2 className="mt-6 text-2xl font-bold text-gray-900">Reservation Confirmed!</h2>
            <p className="mt-2 text-sm text-gray-600">
              We look forward to hosting you for <span className="text-[#f47b20] font-bold">{guests} guests</span> on{' '}
              <span className="text-[#f47b20] font-bold">{date}</span> at{' '}
              <span className="text-[#f47b20] font-bold">{timeSlot}</span> in {seatingZone}.
            </p>
            <div className="mt-8 flex justify-center gap-4">
              <Link
                to="/menu"
                className="rounded-md bg-[#f47b20] px-6 py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
              >
                Pre-order Menu Items
              </Link>
              <button
                onClick={() => setIsSubmitted(false)}
                className="rounded-md border border-gray-300 bg-gray-50 px-6 py-3 text-xs font-bold text-gray-700 hover:bg-gray-100"
              >
                Book Another Table
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
            {/* Guest Count */}
            <div>
              <label className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
                <Users size={16} className="text-[#f47b20]" /> Number of Guests
              </label>
              <div className="flex flex-wrap gap-3">
                {[1, 2, 3, 4, 5, 6, 8, 10].map((num) => (
                  <button
                    type="button"
                    key={num}
                    onClick={() => setGuests(num)}
                    className={`h-11 w-12 rounded-lg text-xs font-bold transition ${
                      guests === num
                        ? 'bg-[#f47b20] text-white shadow-sm scale-105'
                        : 'border border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {num} {num === 10 ? '+' : ''}
                  </button>
                ))}
              </div>
            </div>

            {/* Date & Time Slot */}
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
                  <Calendar size={16} className="text-[#f47b20]" /> Select Date
                </label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>

              <div>
                <label className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
                  <Clock size={16} className="text-[#f47b20]" /> Available Time Slot
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {timeSlots.map((slot) => (
                    <button
                      type="button"
                      key={slot}
                      onClick={() => setTimeSlot(slot)}
                      className={`rounded-md py-2 text-xs font-bold transition ${
                        timeSlot === slot
                          ? 'bg-[#f47b20] text-white'
                          : 'border border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Seating Preference */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 block">Seating Area</label>
              <div className="grid gap-4 md:grid-cols-3">
                {seatingOptions.map((opt) => (
                  <div
                    key={opt.name}
                    onClick={() => setSeatingZone(opt.name)}
                    className={`cursor-pointer rounded-xl border p-4 transition ${
                      seatingZone === opt.name
                        ? 'border-[#f47b20] bg-orange-50/60 shadow-sm'
                        : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                    }`}
                  >
                    <p className="font-bold text-gray-900 text-xs">{opt.name}</p>
                    <p className="mt-1 text-[11px] text-gray-500">{opt.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Special Request */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2 block">Special Requests (Optional)</label>
              <textarea
                rows={3}
                placeholder="Anniversary celebration, dietary preferences, high-chair needed..."
                value={specialRequest}
                onChange={(e) => setSpecialRequest(e.target.value)}
                className="w-full rounded-md border border-gray-300 bg-white p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-md bg-[#f47b20] py-3.5 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f]"
            >
              Confirm Table Reservation
            </button>
          </form>
        )}
      </main>
    </div>
  )
}
