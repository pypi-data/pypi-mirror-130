#!/usr/bin/env bash

FABRIC_COMPAT_PATH="."
FABRIC_COMPAT_TASKS=""

fabric_compat:task_exists() {
    if [ -z "${1:-}" ]
    then
        echo "Usage: fabric_compat:task_exists <taskname>"
        return 1
    fi
    if [ -z "${FABRIC_COMPAT_TASKS}" ]
    then
        if [ ! -e 'fabfile.py' ]
        then
            b5:abort "No fabfile.py found"
        fi

        FABRIC_COMPAT_TASKS="$( fabric_compat:run --shortlist )"
    fi

    if ( echo "${FABRIC_COMPAT_TASKS}" | grep -q -e "^$1$" )
    then
        return 0
    else
        return 1
    fi
}

fabric_compat:run() {
    (
        cd "${FABRIC_COMPAT_PATH}" && \
        fab "$@"
    )
}

task:fab() {
    fabric_compat:run "$@"
}

fabric_compat:install() {
    if fabric_compat:task_exists 'setup'
    then
        fabric_compat:run setup
    fi
}

fabric_compat:update() {
    if fabric_compat:task_exists 'install'
    then
        fabric_compat:run install
    fi
    if fabric_compat:task_exists 'install_js'
    then
        fabric_compat:run install_js
    fi
}

# COMMON TASKS

if fabric_compat:task_exists 'css'
then
    task:css() {
        fabric_compat:run css
    }
fi

if fabric_compat:task_exists 'watch'
then
    task:watch() {
        fabric_compat:run watch
    }
fi

if fabric_compat:task_exists 'deploy'
then
    task:deploy() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy:"${2:-}"
    }
fi

if fabric_compat:task_exists 'deploy_setup'
then
    task:deploy_install() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_setup
    }
fi

# MORE TASKS FOUND IN PROJECTS

if fabric_compat:task_exists 'compilemessages'
then
    task:compilemessages() {
        (
            if [ -d /usr/local/opt/gettext/bin ]
            then
                PATH="/usr/local/opt/gettext/bin:$PATH"
            fi
            fabric_compat:run compilemessages
        )
    }
fi

if fabric_compat:task_exists 'makemessages'
then
    task:makemessages() {
        (
            if [ -d /usr/local/opt/gettext/bin ]
            then
                PATH="/usr/local/opt/gettext/bin:$PATH"
            fi
            fabric_compat:run makemessages
        )
    }
fi

if fabric_compat:task_exists 'deploy_apply_files'
then
    task:deploy_apply_files() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_apply_files
    }
fi

if fabric_compat:task_exists 'deploy_files'
then
    task:deploy_files() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_files
    }
fi

if fabric_compat:task_exists 'deploy_migrate'
then
    task:deploy_migrate() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_migrate
    }
fi

if fabric_compat:task_exists 'deploy_push_files'
then
    task:deploy_push_files() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_push_files
    }
fi

if fabric_compat:task_exists 'deploy_restart'
then
    task:deploy_restart() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_restart
    }
fi

if fabric_compat:task_exists 'deploy_start'
then
    task:deploy_start() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_start
    }
fi

if fabric_compat:task_exists 'deploy_static'
then
    task:deploy_static() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_static
    }
fi

if fabric_compat:task_exists 'deploy_stop'
then
    task:deploy_stop() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_stop
    }
fi

if fabric_compat:task_exists 'migrate'
then
    task:migrate() {
        fabric_compat:run migrate
    }
fi

if fabric_compat:task_exists 'run'
then
    task:run() {
        fabric_compat:run run
    }
fi

if fabric_compat:task_exists 'rundev'
then
    task:rundev() {
        fabric_compat:run rundev
    }
fi

if fabric_compat:task_exists 'shell'
then
    task:shell() {
        fabric_compat:run shell
    }
fi

if fabric_compat:task_exists 'static'
then
    task:static() {
        fabric_compat:run static
    }
fi

if fabric_compat:task_exists 'syncdb'
then
    task:syncdb() {
        fabric_compat:run syncdb
    }
fi

if fabric_compat:task_exists 'browsersync'
then
    task:browsersync() {
        fabric_compat:run browsersync:"${1:-}"
    }
fi

if fabric_compat:task_exists 'icons'
then
    task:icons() {
        fabric_compat:run icons
    }
fi

if fabric_compat:task_exists 'deploy_clear_cache'
then
    task:deploy_clear_cache() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_clear_cache
    }
fi

if fabric_compat:task_exists 'deploy_database_compare'
then
    task:deploy_database_compare() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_database_compare
    }
fi

if fabric_compat:task_exists 'deploy_enable_install_tool'
then
    task:deploy_enable_install_tool() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_enable_install_tool
    }
fi

if fabric_compat:task_exists 'deploy_disable_install_tool'
then
    task:deploy_disable_install_tool() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_disable_install_tool
    }
fi

if fabric_compat:task_exists 'deploy_maintenance_enable'
then
    task:deploy_maintenance_enable() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_maintenance_enable
    }
fi

if fabric_compat:task_exists 'deploy_maintenance_disable'
then
    task:deploy_maintenance_disable() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_maintenance_disable
    }
fi

if fabric_compat:task_exists 'deploy_cc'
then
    task:deploy_cc() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_cc
    }
fi

if fabric_compat:task_exists 'deploy_drush'
then
    task:deploy_drush() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_drush:"${2:-}"
    }
fi

if fabric_compat:task_exists 'deploy_apply_migrations'
then
    task:deploy_apply_migrations() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_apply_migrations
    }
fi

if fabric_compat:task_exists 'deploy_reindex'
then
    task:deploy_reindex() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_reindex
    }
fi

if fabric_compat:task_exists 'deploy_maintenance_on'
then
    task:deploy_maintenance_on() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_maintenance_on
    }
fi

if fabric_compat:task_exists 'deploy_maintenance_off'
then
    task:deploy_maintenance_off() {
        if [ -z "${1:-}" ]
        then
            echo "No target given, aborting"
            exit 1
        fi
        fabric_compat:run "$1" deploy_maintenance_off
    }
fi
