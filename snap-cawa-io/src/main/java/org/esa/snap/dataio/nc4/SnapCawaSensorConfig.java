package org.esa.beam.dataio.nc4;

import java.util.List;

/**
 * todo: add comment
 * To change this template use File | Settings | File Templates.
 * Date: 12.11.2015
 * Time: 13:57
 *
 * @author olafd
 */
public class SnapCawaSensorConfig {
    private List<String> meanBandNames;
    private List<String> uncertaintyBandNames;

    public static SnapCawaSensorConfig create(String sensor, String spatialResolution) {
        // todo if needed
        return null;
    }

    public List<String> getMeanBandNames() {
        // todo
        return meanBandNames;
    }

    public List<String> getUncertaintyBandNames() {
        // todo
        return uncertaintyBandNames;
    }
}
