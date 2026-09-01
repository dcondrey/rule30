#!/bin/zsh
# Launch the full OpenEvolve P3 search with a HARD wall-clock ceiling.
#
# macOS here has neither `timeout` nor `gtimeout`, so the ceiling is enforced
# by an explicit watchdog: the search runs in the background, a sleeper kills
# the whole process group after CEILING_SECONDS, and checkpointing (see
# config_full.yaml checkpoint_interval) makes the kill leave a usable state.
#
# RULE30_P3_PROFILE=smoke is exported so OpenEvolve's evaluation worker
# processes inherit it. "smoke" is the only profile with a measured baseline
# in baseline_exponent.json AND the only one validated against the sanity
# candidates; "tiny" exponents are explicitly untrustworthy and "full" would
# need a fresh multi-hour baseline measurement. See PREREGISTRATION.md.
set -u

HERE=${0:A:h}
cd "$HERE"

CEILING_SECONDS=${CEILING_SECONDS:-21600}   # 6 hours
OUT=${OUT:-openevolve_output_full}
LOG=${LOG:-$HERE/full_run.log}

export RULE30_P3_PROFILE=smoke

PY=$HERE/vendor/openevolve/.venv/bin/python

echo "=== launch $(date) ceiling=${CEILING_SECONDS}s profile=$RULE30_P3_PROFILE ===" >> "$LOG"
echo "=== load at launch: $(uptime) ===" >> "$LOG"

"$PY" "$HERE/vendor/openevolve/openevolve-run.py" \
    "$HERE/initial_program.py" \
    "$HERE/evaluator.py" \
    --config "$HERE/config_full.yaml" \
    --output "$HERE/$OUT" \
    >> "$LOG" 2>&1 &
RUN_PID=$!
echo "search pid=$RUN_PID" >> "$LOG"
echo "$RUN_PID" > "$HERE/.full_run.pid"

# Watchdog: hard ceiling.
(
  sleep "$CEILING_SECONDS"
  if kill -0 "$RUN_PID" 2>/dev/null; then
    echo "=== WALL-CLOCK CEILING HIT at $(date); terminating pid $RUN_PID ===" >> "$LOG"
    kill -TERM "$RUN_PID" 2>/dev/null
    sleep 30
    kill -KILL "$RUN_PID" 2>/dev/null
    pkill -KILL -P "$RUN_PID" 2>/dev/null
  fi
) &
echo "watchdog pid=$!" >> "$LOG"

wait "$RUN_PID"
RC=$?
echo "=== search exited rc=$RC at $(date) ===" >> "$LOG"
