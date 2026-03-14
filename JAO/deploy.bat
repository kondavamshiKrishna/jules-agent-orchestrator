@echo off
echo ========================================================
echo Deploying JAO to your Official Docker Desktop Environment
echo ========================================================

echo.
echo [1/2] Stopping any old containers...
docker compose down
if %errorlevel% neq 0 (
    docker-compose down
)

echo.
echo [2/2] Building and starting JAO Containers (jao-backend, jao-frontend)...
docker compose up --build -d
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] 'docker compose' failed. Trying legacy 'docker-compose' command...
    docker-compose up --build -d
)

echo.
echo ========================================================
echo Deployment command complete! 
echo Please check your Docker Desktop GUI. You should see instances 
echo named 'jao-backend' and 'jao-frontend' running.
echo.
echo If you see errors above, please copy and paste them into our chat!
echo ========================================================
pause
