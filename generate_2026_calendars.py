#!/usr/bin/env python3
"""
Legislative Calendar ICS Generator - 2026 Edition v4 (With State Abbreviations)
Generates ICS calendar files showing session periods as multi-day blocks
Groups consecutive session days together for cleaner calendar display
Uses postal abbreviations for state calendar titles
"""

import os
from datetime import datetime, timedelta, date
from icalendar import Calendar, Event
import pytz

# State postal abbreviations
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Federal holidays for 2026
FEDERAL_HOLIDAYS_2026 = [
    date(2026, 1, 1),   # New Year's Day
    date(2026, 1, 19),  # Martin Luther King Jr. Day
    date(2026, 2, 16),  # Presidents' Day
    date(2026, 5, 25),  # Memorial Day
    date(2026, 7, 3),   # Independence Day (observed Friday)
    date(2026, 9, 7),   # Labor Day
    date(2026, 10, 12), # Columbus Day
    date(2026, 11, 11), # Veterans Day
    date(2026, 11, 26), # Thanksgiving
    date(2026, 11, 27), # Day after Thanksgiving
    date(2026, 12, 25), # Christmas
]

# Session data for 2026
LEGISLATIVE_SESSIONS_2026 = {
    'US_House': {
        'name': 'U.S. House of Representatives',
        'start_date': '2026-01-06',
        'end_date': '2026-12-31',
        'description': '120th Congress, 1st Session',
        'recess_periods': [
            ('2026-02-14', '2026-02-22'),  # Presidents' Day Recess
            ('2026-03-28', '2026-04-12'),  # Spring Recess
            ('2026-05-23', '2026-05-31'),  # Memorial Day Recess
            ('2026-07-04', '2026-09-07'),  # Summer District Work Period
            ('2026-11-21', '2026-11-29'),  # Thanksgiving Recess
            ('2026-12-19', '2026-12-31'),  # Year-end Recess
        ]
    },
    'US_Senate': {
        'name': 'U.S. Senate',
        'start_date': '2026-01-06',
        'end_date': '2026-12-31',
        'description': '120th Congress, 1st Session',
        'recess_periods': [
            ('2026-02-14', '2026-02-22'),  # Presidents' Day Recess
            ('2026-03-28', '2026-04-12'),  # Spring Recess
            ('2026-05-23', '2026-05-31'),  # Memorial Day Recess
            ('2026-07-04', '2026-09-07'),  # Summer Recess
            ('2026-11-21', '2026-11-29'),  # Thanksgiving Recess
            ('2026-12-19', '2026-12-31'),  # Year-end Recess
        ]
    },
    'California': {
        'name': 'California State Legislature',
        'start_date': '2026-01-05',
        'end_date': '2026-08-31',
        'description': '2025-2026 Regular Session (Even year)',
        'recess_periods': [
            ('2026-02-16', '2026-02-22'),  # Presidents' Day Recess
            ('2026-04-06', '2026-04-12'),  # Spring Recess
            ('2026-07-04', '2026-07-12'),  # July 4th Recess
        ]
    },
    'Indiana': {
        'name': 'Indiana General Assembly',
        'start_date': '2026-01-05',
        'end_date': '2026-03-14',
        'description': '2026 Regular Session (30 days - even year)',
        'recess_periods': []
    },
    'Missouri': {
        'name': 'Missouri General Assembly',
        'start_date': '2026-01-07',
        'end_date': '2026-05-15',
        'description': '2026 Regular Session',
        'recess_periods': [
            ('2026-03-16', '2026-03-22'),  # Spring Break
        ]
    },
    'Georgia': {
        'name': 'Georgia General Assembly',
        'start_date': '2026-01-12',
        'end_date': '2026-04-06',
        'description': '2026 Regular Session (40 legislative days)',
        'recess_periods': []
    },
    'South_Carolina': {
        'name': 'South Carolina General Assembly',
        'start_date': '2026-01-13',
        'end_date': '2026-05-07',
        'description': '2026 Regular Session',
        'recess_periods': []
    },
    'Alabama': {
        'name': 'Alabama Legislature',
        'start_date': '2026-01-13',
        'end_date': '2026-03-27',
        'description': '2026 Regular Session (30 legislative days)',
        'recess_periods': []
    },
    'Virginia': {
        'name': 'Virginia General Assembly',
        'start_date': '2026-01-14',
        'end_date': '2026-03-14',
        'description': '2026 Regular Session (60 calendar days - even year)',
        'recess_periods': []
    }
}

def get_state_abbrev(state_name):
    """Get postal abbreviation for a state, or return the state name if not found"""
    # Extract just the state name (e.g., "California" from "California State Legislature")
    for state, abbrev in STATE_ABBREV.items():
        if state in state_name:
            return abbrev
    return state_name

def is_weekday(check_date):
    """Check if date is a weekday (Monday-Friday)"""
    return check_date.weekday() < 5

def is_in_recess(check_date, recess_periods):
    """Check if date falls within any recess period"""
    for start_str, end_str in recess_periods:
        start = datetime.strptime(start_str, '%Y-%m-%d').date()
        end = datetime.strptime(end_str, '%Y-%m-%d').date()
        if start <= check_date <= end:
            return True
    return False

def generate_session_days(session_data):
    """Generate list of actual session days (weekdays, not holidays, not in recess)"""
    start_date = datetime.strptime(session_data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(session_data['end_date'], '%Y-%m-%d').date()
    recess_periods = session_data.get('recess_periods', [])
    
    session_days = []
    current_date = start_date
    
    while current_date <= end_date:
        # Include only if: weekday, not a federal holiday, not in recess
        if (is_weekday(current_date) and 
            current_date not in FEDERAL_HOLIDAYS_2026 and 
            not is_in_recess(current_date, recess_periods)):
            session_days.append(current_date)
        
        current_date += timedelta(days=1)
    
    return session_days

def group_consecutive_days(session_days):
    """Group consecutive session days into blocks"""
    if not session_days:
        return []
    
    blocks = []
    current_block_start = session_days[0]
    current_block_end = session_days[0]
    
    for i in range(1, len(session_days)):
        # Check if this day is consecutive (next day after current_block_end)
        if session_days[i] == current_block_end + timedelta(days=1):
            # Extend the current block
            current_block_end = session_days[i]
        else:
            # Gap found - save current block and start new one
            blocks.append((current_block_start, current_block_end))
            current_block_start = session_days[i]
            current_block_end = session_days[i]
    
    # Don't forget the last block
    blocks.append((current_block_start, current_block_end))
    
    return blocks

def create_session_block_event(session_id, session_name, block_start, block_end, block_num):
    """Create an all-day event for a session block"""
    event = Event()
    
    # ICS end dates are exclusive, so add one day
    ics_end_date = block_end + timedelta(days=1)
    
    # Calculate number of days in block
    num_days = (block_end - block_start).days + 1
    
    # Get state abbreviation if it's a state
    state_abbrev = get_state_abbrev(session_name)
    
    if num_days == 1:
        summary = f"{state_abbrev} - In Session"
    else:
        summary = f"{state_abbrev} - In Session ({num_days} days)"
    
    event.add('summary', summary)
    event.add('dtstart', block_start)
    event.add('dtend', ics_end_date)
    event.add('description', f"Legislature in session")
    event.add('uid', f'{session_id}-2026-block-{block_num}@legislative-calendar.beekeepergroup.com')
    event.add('dtstamp', datetime.now(pytz.UTC))
    
    # Mark as transparent so it doesn't block calendars
    event.add('transp', 'TRANSPARENT')
    
    return event

def generate_calendar(sessions_to_include, output_filename, calendar_title=None):
    """Generate an ICS calendar file for specified sessions"""
    cal = Calendar()
    
    # Determine calendar title
    if calendar_title is None:
        if len(sessions_to_include) == 1:
            session_data = LEGISLATIVE_SESSIONS_2026[sessions_to_include[0]]
            state_abbrev = get_state_abbrev(session_data['name'])
            calendar_title = f"{state_abbrev} - 2026 Legislative Session"
        else:
            calendar_title = "Legislative Sessions Calendar 2026"
    
    # Calendar metadata
    cal.add('prodid', '-//Beekeeper Group//Legislative Calendar 2026//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', calendar_title)
    cal.add('x-wr-timezone', 'America/New_York')
    cal.add('x-wr-caldesc', 'Legislative session periods (excludes weekends, holidays, recesses)')
    
    total_blocks = 0
    total_days = 0
    
    # Add events for each session
    for session_id in sessions_to_include:
        if session_id not in LEGISLATIVE_SESSIONS_2026:
            print(f"Warning: Session {session_id} not found in data")
            continue
            
        session_data = LEGISLATIVE_SESSIONS_2026[session_id]
        session_days = generate_session_days(session_data)
        session_blocks = group_consecutive_days(session_days)
        
        for block_num, (block_start, block_end) in enumerate(session_blocks):
            event = create_session_block_event(
                session_id, 
                session_data['name'], 
                block_start, 
                block_end,
                block_num
            )
            cal.add_component(event)
        
        total_blocks += len(session_blocks)
        total_days += len(session_days)
        print(f"  {session_data['name']}: {len(session_blocks)} blocks, {len(session_days)} session days")
    
    # Write to file
    with open(output_filename, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"✓ Generated: {output_filename} ({total_blocks} blocks, {total_days} total days)")
    return output_filename

def main():
    """Main function to generate all calendar files"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    print("Legislative Calendar Generator - 2026 Edition v4")
    print("Multi-day Session Blocks (with State Abbreviations)")
    print("=" * 70)
    print()
    
    # Generate combined federal calendar
    print("Generating Federal Legislative Calendar...")
    generate_calendar(
        ['US_House', 'US_Senate'],
        'output/federal_legislative_calendar_2026.ics',
        'Federal - 2026 Legislative Session'
    )
    print()
    
    # Generate individual state calendars
    print("Generating State Legislative Calendars...")
    states = ['California', 'Indiana', 'Missouri', 'Georgia', 'South_Carolina', 'Alabama', 'Virginia']
    for state in states:
        session_data = LEGISLATIVE_SESSIONS_2026[state]
        state_abbrev = get_state_abbrev(session_data['name'])
        print(f"\n{session_data['name']} ({state_abbrev}):")
        generate_calendar(
            [state],
            f'output/{state.lower()}_legislative_calendar_2026.ics',
            f'{state_abbrev} - 2026 Legislative Session'
        )
    print()
    
    # Generate combined calendar (all sessions)
    print("Generating Combined Federal + State Calendar...")
    all_sessions = ['US_House', 'US_Senate'] + states
    generate_calendar(
        all_sessions,
        'output/all_legislative_sessions_2026.ics',
        'All Legislative Sessions - 2026'
    )
    print()
    
    print("=" * 70)
    print("✓ All 2026 calendars generated successfully!")
    print()
    print("Calendar features:")
    print("  ✓ State postal abbreviations in titles (e.g., 'AL - 2026 Legislative Session')")
    print("  ✓ Consecutive session days grouped into multi-day blocks")
    print("  ✓ Weekdays only (Mon-Fri)")
    print("  ✓ Federal holidays excluded")
    print("  ✓ Recess periods excluded")
    print()
    print("Next steps:")
    print("  1. git add output/*.ics generate_2026_calendars_v4.py")
    print("  2. git commit -m 'Add state abbreviations to calendar titles'")
    print("  3. git push")
    print("  4. Google Calendar will auto-update within 24 hours")

if __name__ == '__main__':
    main()
