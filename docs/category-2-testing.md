# Category 2 - Patient, Provider and Nursing Operations

Category 2 adds real provider-quality and nurse home-care workflows on top of the stabilized Category 1 foundation.

## Delivered
- richer provider professional profiles: gender, age-derived DOB, title, qualifications, languages, experience, location, consultation modes and home-care radius
- verified-provider discovery only
- completed CareLink case counts and verified-patient ratings
- one review per completed appointment
- service-issue/complaint records separated from star reviews
- provider quality metrics for completed appointments/home visits, ratings, complaints and cancellations
- nurse home-visit check-in, care record, escalation and check-out
- patient provider-details and verified-review screens
- nurse care-session screen
- automated Category 2 API tests

## Safety and privacy
Public provider age is derived from date of birth; date of birth itself is not returned in patient discovery. Provider verification remains pending until an authorized verification workflow confirms credentials. No external regulator is simulated as successful.

## Local test
    cd backend
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements-dev.txt
    python -m alembic upgrade head
    pytest -q

Then:
    cd ..\mobile
    npm install
    npx expo install --fix
    npm run typecheck

Start patient and provider separately with npm run patient and npm run provider.
