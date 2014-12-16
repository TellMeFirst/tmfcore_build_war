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

import it.polito.tellmefirst.classify.Classifier;
import it.polito.tellmefirst.util.TMFVariables;
import it.polito.tellmefirst.lucene.IndexesUtil;
import java.util.List;
import static java.util.stream.Collectors.toList;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.Consumes;
import javax.ws.rs.core.MediaType;

@Path("classify")
public class ClassifyResource {

	private final TMFVariables variables;

	public ClassifyResource() {
		variables = new TMFVariables(
			"/var/local/tmfcore/conf/server.properties");
		IndexesUtil.init();
	}

	@POST
	@Path("json")
	@Produces(MediaType.APPLICATION_JSON)
	@Consumes(MediaType.APPLICATION_JSON)
	public List<ClassifyOutput> classifyJson(ClassifyInput input) {
		return jsonAdapter(new Classifier(input.getLang())
				.classify(input.getText(), input.getNumTopics()));
	}

	private List<ClassifyOutput> jsonAdapter(List<String[]> list) {
		return list.stream().map(strings -> {
			ClassifyOutput output = new ClassifyOutput();
			output.setUri(strings[0]);
			output.setLabel(strings[1]);
			output.setTitle(strings[2]);
			output.setScore(strings[3]);
			output.setMergedTypes(strings[4]);
			output.setImage(strings[5]);
			output.setWikilink(strings[6]);
			return output;
		}).collect(toList());
	}
}
