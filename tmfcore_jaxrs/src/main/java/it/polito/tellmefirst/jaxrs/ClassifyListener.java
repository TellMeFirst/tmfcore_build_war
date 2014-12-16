/*-
 * Copyright (C) 2014 Riccardo Muzzì.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package it.polito.tellmefirst.jaxrs;

import it.polito.tellmefirst.lucene.IndexesUtil;
import static it.polito.tellmefirst.util.TMFUtils.unchecked;
import it.polito.tellmefirst.util.TMFVariables;
import java.io.IOException;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;

@WebListener
public class ClassifyListener implements ServletContextListener {

	private TMFVariables variables;

	private void classifyResource() throws IOException {
		variables = new TMFVariables(
			"/var/local/tmfcore/conf/server.properties");
		IndexesUtil.init();
	}
	
	@Override
	public void contextInitialized(ServletContextEvent sce) {
		unchecked( this::classifyResource );
	}

	@Override
	public void contextDestroyed(ServletContextEvent sce) {
	}

}
