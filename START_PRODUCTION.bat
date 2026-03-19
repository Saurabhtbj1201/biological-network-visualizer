@echo off
REM ============================================
REM NetworkInsight Production Deployment Script
REM ============================================
REM This script starts the production-ready stack

setlocal enabledelayedexpansion

echo.
echo ======== NetworkInsight Production Launcher ========
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker is not installed or not in PATH
    echo.
    echo Install Docker from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo ✅ Docker found: %docker%

REM Check if docker compose is available
docker compose version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker Compose is not available
    echo.
    echo Make sure Docker Desktop (which includes Compose) is installed
    echo.
    pause
    exit /b 1
)

echo ✅ Docker Compose is available

echo.
echo ======== Checking Current Status ========
echo.

REM Check if services are already running
docker compose ps >nul 2>&1
if errorlevel 0 (
    echo Current running services:
    docker compose ps
    echo.
    set /p choice="Services are already running. (S)top them, (R)estart, or (C)ontinue? [s/r/c]: "
    if /i "!choice!"=="s" (
        echo Stopping services...
        docker compose stop
        echo ✅ Services stopped
    ) else if /i "!choice!"=="r" (
        echo Restarting services...
        docker compose restart
        goto check_services
    ) else (
        goto check_services
    )
)

echo.
echo ======== Building & Starting Services ========
echo.

REM Build and start containers
echo Building Docker images...
docker compose build
if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo Starting services...
docker compose up -d
if errorlevel 1 (
    echo ❌ Failed to start services
    echo.
    echo Troubleshooting:
    echo 1. Check ports are not in use: netstat -ano ^| findstr :3000 :5000 :5432
    echo 2. Check Docker daemon is running
    echo 3. Try: docker compose logs
    echo.
    pause
    exit /b 1
)

echo ✅ Services started

:check_services
echo.
echo ======== Waiting for Services to be Ready ========
echo.

REM Wait for services to be healthy
echo Waiting for PostgreSQL...
timeout /t 5 /nobreak
docker compose exec -T postgres pg_isready -U networkinsight >nul 2>&1
:wait_pg
if errorlevel 1 (
    timeout /t 2 /nobreak
    docker compose exec -T postgres pg_isready -U networkinsight >nul 2>&1
    if errorlevel 1 goto wait_pg
)
echo ✅ PostgreSQL is ready

echo Waiting for Redis...
docker compose exec -T redis redis-cli ping >nul 2>&1
:wait_redis
if errorlevel 1 (
    timeout /t 2 /nobreak
    docker compose exec -T redis redis-cli ping >nul 2>&1
    if errorlevel 1 goto wait_redis
)
echo ✅ Redis is ready

echo Waiting for Backend...
timeout /t 3 /nobreak
echo ✅ Backend starting

echo Waiting for Frontend...
timeout /t 3 /nobreak
echo ✅ Frontend starting

echo.
echo ======== Services Status ========
echo.
docker compose ps

echo.
echo ======== All Systems GO! ========
echo.
echo ✅ Frontend:     http://localhost:3000
echo ✅ Backend:      http://localhost:5000
echo ✅ Database:     localhost:5432
echo ✅ Cache:        localhost:6379
echo.

echo Ready to use! Quick test:
echo   - Open http://localhost:3000 in browser
echo   - Or run: curl http://localhost:5000/health
echo.

echo View logs with: docker compose logs -f [service]
echo Services: postgres, redis, backend, frontend
echo.

echo Stop services: docker compose stop
echo View everything: docker compose ps -a
echo.

pause
